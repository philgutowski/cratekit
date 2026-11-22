#!/usr/bin/env python3
"""Rebuild ``src/cratekit/_vendor/downloader/`` from an upstream source distribution.

KTD4 vendors the downloader as a source tree because its upstream left GitHub and
PyPI in December 2025. The patches are declared as exact expected text, and a
patch whose anchor is missing ABORTS the re-vendor rather than being skipped, so
a bump cannot silently drop one. ``vendor/README.md`` records each patch's reason
and where the known good upstream copies live (the artifact is not committed).

Usage::

    python scripts/revendor_downloader.py path/to/tidal_dl_ng-<version>.tar.gz
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VENDOR_PACKAGE = REPO_ROOT / "src" / "cratekit" / "_vendor" / "downloader"
VENDOR_LICENSE_COPY = REPO_ROOT / "vendor" / "LICENSE.downloader"

UPSTREAM_PACKAGE = "tidal_dl_ng"
VENDORED_IMPORT_ROOT = "cratekit._vendor.downloader"

# Reduction 1: the GUI half imports PySide6, an optional upstream extra, at module
# scope, so a headless install cannot import any of it.
DROP_GUI = ("gui.py", "logger.py", "dialog.py", "worker.py", "helper/gui.py", "ui")

# Reduction 2: api.py carries plaintext third party OAuth client pairs (R1), raises
# at import in 0.33.0, and nothing imports it. The secret scan misses its camelCase
# JSON keys, so dropping it is the only guard.
DROP_CREDENTIAL_CARRIERS = ("api.py",)


class PatchError(RuntimeError):
    """A declared patch did not find the text it was written against."""


class _Declared:
    """Shared by the patch kinds: the file a patch targets must exist."""

    relative_path: str
    why: str

    def _target(self, root: Path) -> Path:
        target = root / self.relative_path
        if not target.is_file():
            raise PatchError(f"{self.relative_path} is not in the extracted tree; {self.why}")
        return target


class Patch(_Declared):
    """One exact text substitution; ``old`` must appear EXACTLY ONCE."""

    def __init__(self, relative_path: str, old: str, new: str, why: str) -> None:
        self.relative_path = relative_path
        self.old = old
        self.new = new
        self.why = why

    def apply(self, root: Path) -> None:
        target = self._target(root)
        text = target.read_text(encoding="utf-8")
        count = text.count(self.old)
        if count != 1:
            raise PatchError(
                f"{self.relative_path}: expected exactly 1 occurrence of the patch "
                f"anchor, found {count}. Upstream changed under this patch. "
                f"Re-derive it by hand; do NOT skip it. The patch exists because: {self.why}"
            )
        target.write_text(text.replace(self.old, self.new), encoding="utf-8")


class LinePatch(_Declared):
    """Replace a WHOLE line matched by its leading text, so a credential's literal goes
    with it and this script never spells a secret to delete it."""

    def __init__(self, relative_path: str, prefix: str, replacement: str, why: str) -> None:
        self.relative_path = relative_path
        self.prefix = prefix
        self.replacement = replacement
        self.why = why

    def apply(self, root: Path) -> None:
        target = self._target(root)
        lines = target.read_text(encoding="utf-8").splitlines(keepends=True)
        hits = [i for i, line in enumerate(lines) if line.lstrip().startswith(self.prefix)]
        if len(hits) != 1:
            raise PatchError(
                f"{self.relative_path}: expected exactly 1 line starting with "
                f"{self.prefix!r}, found {len(hits)}. Upstream changed under this "
                f"patch. Re-derive it by hand; do NOT skip it. It exists because: {self.why}"
            )
        lines[hits[0]] = self.replacement
        target.write_text("".join(lines), encoding="utf-8")


class SpanPatch(_Declared):
    """Replace everything from one anchor up to the next, exclusive; each once."""

    def __init__(
        self, relative_path: str, start: str, end: str, replacement: str, why: str
    ) -> None:
        self.relative_path = relative_path
        self.start = start
        self.end = end
        self.replacement = replacement
        self.why = why

    def apply(self, root: Path) -> None:
        target = self._target(root)
        text = target.read_text(encoding="utf-8")
        for anchor in (self.start, self.end):
            if text.count(anchor) != 1:
                raise PatchError(
                    f"{self.relative_path}: anchor {anchor!r} occurs "
                    f"{text.count(anchor)} times, expected 1. Upstream changed under "
                    f"this patch. Re-derive it; do NOT skip it. It exists because: {self.why}"
                )
        head, _, rest = text.partition(self.start)
        _, _, tail = rest.partition(self.end)
        target.write_text(head + self.replacement + self.end + tail, encoding="utf-8")


# Patch 1: the Dolby Atmos client credentials are emptied (R1); the text says why.
PATCH_ATMOS_CREDENTIALS = Patch(
    relative_path="constants.py",
    old="# Dolby Atmos API credentials (obfuscated)\n",
    new=(
        "# Dolby Atmos API credentials: REMOVED WHEN VENDORED (Cratekit patch).\n"
        "#\n"
        "# Upstream ships a third-party streaming client id and client secret here,\n"
        "# base64-encoded and split across concatenated literals. Cratekit ships no\n"
        "# credential material (R1), so both are empty. The Atmos session switch\n"
        "# therefore fails its login and returns False, which the download path\n"
        "# already handles.\n"
        "#\n"
        "# Nothing is lost: the Atmos path is gated on a setting that defaults to\n"
        "# False and requests Quality.low_320k, which R21's lossless policy refuses.\n"
    ),
    why="R1 forbids shipping credential material, encoded or not",
)

PATCH_ATMOS_ID = LinePatch(
    relative_path="constants.py",
    prefix="ATMOS_ID_B64 =",
    replacement='ATMOS_ID_B64 = ""  # emptied when vendored (Cratekit patch, R1)\n',
    why="R1 forbids shipping credential material, encoded or not",
)
PATCH_ATMOS_SECRET = LinePatch(
    relative_path="constants.py",
    prefix="ATMOS_SECRET_B64 =",
    replacement='ATMOS_SECRET_B64 = ""  # emptied when vendored (Cratekit patch, R1)\n',
    why="R1 forbids shipping credential material, encoded or not",
)

# Patch 2: the commented out plaintext credential pair in config.py, which a
# scanner cannot tell from a live one.
PATCH_COMMENTED_CLIENT_ID = LinePatch(
    relative_path="config.py",
    prefix="# self.session.config.client_id =",
    replacement=(
        "        # A commented-out plaintext client id was removed here when vendored\n"
        "        # (Cratekit patch, R1). A scanner cannot tell a commented credential\n"
        "        # from a live one, and neither can a reader skimming a diff.\n"
    ),
    why="R1 forbids shipping credential material, including commented-out material",
)
PATCH_COMMENTED_CLIENT_SECRET = LinePatch(
    relative_path="config.py",
    prefix="# self.session.config.client_secret =",
    replacement="        # A commented-out plaintext client secret was removed here too.\n",
    why="R1 forbids shipping credential material, including commented-out material",
)

# Patch 3: the version is pinned, rather than read from the nearest pyproject.toml.
def _pinned_metadata_patch(version: str) -> SpanPatch:
    """Replace the whole of ``metadata_project()``, so ``toml`` is no dependency."""
    return SpanPatch(
        relative_path="__init__.py",
        start="def metadata_project() -> ProjectInformation:",
        end="def version_app() -> str:",
        replacement=f'''# Cratekit patch: the version is PINNED at vendoring time.
#
# Upstream discovered it by walking up to three parent directories from its own
# __file__ looking for a pyproject.toml, then reading ["project"]["version"] and
# ["project"]["urls"]["repository"] out of whichever one it found first, with no
# check on whose file that was.
#
# Vendored, the nearest such file is the HOST application's. Reading it would
# raise KeyError at import time, because Cratekit declares no [project.urls] and
# that lookup sits outside upstream's try block, so `import tidal_dl_ng` would
# fail for a reason naming none of this. Today the walk misses Cratekit's
# pyproject.toml by exactly one directory level. A pinned constant does not
# depend on how deep the package happens to sit.
_VENDORED_VERSION = "{version}"
_UPSTREAM_REPOSITORY = "https://github.com/exislow/tidal-dl-ng"


def metadata_project() -> ProjectInformation:
    return ProjectInformation(version=_VENDORED_VERSION, repository_url=_UPSTREAM_REPOSITORY)


''',
        why="vendored code must not read the host application's project metadata",
    )


# The two imports only the removed body used.
PATCH_DROP_TOML_IMPORT = LinePatch(
    relative_path="__init__.py",
    prefix="import toml",
    replacement="# `import toml` removed when vendored: only the replaced "
    "metadata_project() used it.\n",
    why="an unmaintained dependency kept alive only by dead code",
)
PATCH_DROP_PATH_IMPORT = LinePatch(
    relative_path="__init__.py",
    prefix="from pathlib import Path",
    replacement="# `from pathlib import Path` removed when vendored: only the "
    "replaced metadata_project() used it.\n",
    why="an unused import left by the metadata patch",
)


# Patch 4: the on disk application name, which names the state directory, is pinned.
STATE_DIRECTORY_NAME = "cratekit-downloader"
#: The state directory's name before U197, which patch 11 adopts.
STATE_DIRECTORY_NAME_BEFORE = "tidal-dl-ng"

PATCH_DISPLAY_NAME = Patch(
    relative_path="__init__.py",
    old="__name_display__ = name_app()",
    new=(
        "# Cratekit patch: pinned. Derived from __package__ upstream, which vendored\n"
        "# would name the settings, log, and token directory after an import path.\n"
        f'__name_display__ = "{STATE_DIRECTORY_NAME}"'
    ),
    why="the display name is the on-disk state directory, not a label",
)


# Patch 11: the state directory from before U197's rename is adopted. A patch, since
# the tool's own login resolves the directory and runs no Cratekit code.
PATCH_STATE_DIRECTORY_ADOPTION = Patch(
    relative_path="helper/path.py",
    old=(
        "    path_base: str = os.path.join(path_home(), path_config, __name_display__)\n"
        "\n"
        "    return path_base\n"
    ),
    new=f"""    path_base: str = os.path.join(path_home(), path_config, __name_display__)

    # Cratekit patch (U197): adopt the state directory an installation made
    # before the rename, so a token left in it is not stranded. A move, never a
    # copy, so no second plaintext token is made. The new directory wins when
    # both exist, and a move that fails keeps the old one in use.
    path_before: str = os.path.join(path_home(), path_config, "{STATE_DIRECTORY_NAME_BEFORE}")
    if not os.path.lexists(path_base) and os.path.isdir(path_before):
        try:
            os.rename(path_before, path_base)
        except OSError:
            if not os.path.isdir(path_base):
                return path_before

    return path_base
""",
    why="an installation's token, written under the old directory name, is found",
)


# Patch 5: no tempo tag in any of the three containers (R17). The beat grid suite's
# static checker sees only the Vorbis write, not the ID3 call or the MP4 atom.
_R17_NOTE = (
    "        # R17: the tempo tag write was removed when vendored. rekordbox reads\n"
    "        # file tags on import, so writing the provider's BPM here seeds a grid\n"
    "        # by a longer route. Detection octave-folds, so a wrong seed lands the\n"
    "        # grid at half or double time and drags every cue and loop with it.\n"
)

PATCH_R17_VORBIS = LinePatch(
    relative_path="metadata.py",
    prefix='self.m.tags["BPM"]',
    replacement=_R17_NOTE,
    why="R17: no tempo tag reaches a file Cratekit downloads",
)
PATCH_R17_ID3 = LinePatch(
    relative_path="metadata.py",
    prefix="self.m.tags.add(TBPM(",
    replacement=_R17_NOTE,
    why="R17: no tempo tag reaches a file Cratekit downloads",
)
PATCH_R17_MP4 = SpanPatch(
    relative_path="metadata.py",
    start="if self.bpm > 0:",
    end='self.m.tags["----:com.apple.iTunes:initialkey"]',
    replacement="# R17: the MP4 'tmpo' atom write was removed when vendored.\n        ",
    why="R17: no tempo tag reaches a file Cratekit downloads",
)

# Defence in depth where the provider's tempo enters, against a fourth writer.
PATCH_R17_SOURCE = LinePatch(
    relative_path="download.py",
    prefix="bpm=track.bpm",
    replacement="            bpm=0,  # R17: the provider's tempo never enters a tag (Cratekit patch)\n",
    why="R17: the provider's tempo is never carried into metadata at all",
)


# Patches 7, 8 and 9: the login is PKCE and the persisted token says so, since
# the provider serves the device linking client lossy audio (R-196).
PATCH_PKCE_TOKEN_FIELD = Patch(
    relative_path="model/cfg.py",
    old="    expiry_time: float = 0.0\n",
    new="""    expiry_time: float = 0.0
    # Cratekit patch (R-196): whether this token came from a PKCE login.
    #
    # Upstream persists four keys and drops this one, so a PKCE token reloads as
    # a device-flow token and refreshes against the wrong client, which is the
    # client the provider serves lossy audio to. A field the write never stores
    # is a field the read cannot see.
    is_pkce: bool = False
""",
    why="a PKCE token that reloads as a device-flow token refreshes against the "
    "wrong client, and that client is served lossy audio",
)

# Exact text rather than a span, so an upstream change to the body aborts the run.
PATCH_PKCE_TOKEN_PERSIST = Patch(
    relative_path="config.py",
    old='''        self.set_option("expiry_time", self.session.expiry_time)
        self.save()
''',
    new='''        self.set_option("expiry_time", self.session.expiry_time)
        # Cratekit patch (R-196): persist which client minted this session.
        #
        # Written through `self.data` rather than `set_option`, because
        # `set_option` reads the existing value and calls `.lower()` on the
        # incoming one whenever the field is a bool, so a Python bool raises
        # AttributeError there. `is_pkce` is this model's only bool field.
        #
        # The source is the SESSION's flag, not this object's. `login()` calls
        # `login_token()` first, which assigns `self.is_pkce` from its own
        # defaulted argument before any PKCE handshake runs, so reading it here
        # would record every fresh PKCE login as a device-flow one.
        self.data.is_pkce = bool(getattr(self.session, "is_pkce", False))
        self.save()
''',
    why="a persisted session must record which client minted it, or the refresh "
    "goes to the client the provider serves lossy audio to",
)

PATCH_PKCE_LOGIN_REUSE = Patch(
    relative_path="config.py",
    old="""        is_token = self.login_token()
""",
    new='''        # Cratekit patch (R-196): a stored session is reused only when it is
        # already PKCE.
        #
        # The short circuit is the whole point. Upstream reuses ANY loadable
        # token, so on a machine holding a device-flow token this method would
        # report "you are logged in", never reach the PKCE branch below, and hand
        # back the very token the adapter then refuses. That is every machine
        # that ran this tool before the switch, so the documented
        # re-authorisation would have been an unbreakable loop.
        is_token = bool(getattr(self.data, "is_pkce", False)) and self.login_token(
            do_pkce=True
        )
''',
    why="reusing a device-flow token here would make the documented "
    "re-authorisation a loop that can never mint a PKCE session",
)

PATCH_PKCE_LOGIN_MINT = Patch(
    relative_path="config.py",
    old="""            # Login method: Device linking
            self.session.login_oauth_simple(fn_print)
            # Login method: PKCE authorization (was necessary for HI_RES_LOSSLESS streaming earlier)
            # self.session.login_pkce(fn_print)
""",
    new="""            # Cratekit patch (R-196): PKCE is the only login this product
            # offers. Upstream called `login_oauth_simple` (device linking) and
            # carried this call beside it as a comment, so the commented line was
            # the working one and the live one silently produced lossy downloads.
            # There is deliberately no flag preserving the device flow: a flag
            # that preserves it preserves the defect.
            self.session.login_pkce(fn_print)
""",
    why="the device-linking client is served lossy audio, so the only login this "
    "product offers is PKCE",
)


def rewrite_internal_imports(text: str) -> str:
    """Re-root the package's absolute self-imports, one rule at any depth."""
    return text.replace(f"from {UPSTREAM_PACKAGE}", f"from {VENDORED_IMPORT_ROOT}")


def strip_gui_entry_point(text: str) -> str:
    """Remove the CLI's ``gui`` subcommand, whose module is not vendored."""
    marker = '@app.command()\ndef gui(ctx: typer.Context):'
    start = text.find(marker)
    if start == -1:
        raise PatchError(
            "the CLI 'gui' subcommand was not found. Either upstream renamed it, or "
            "the GUI reduction no longer applies. Re-derive before continuing."
        )
    end = text.find("\ndef handle_sigint_term", start)
    if end == -1:
        raise PatchError("could not find the end of the CLI 'gui' subcommand")
    replacement = (
        "# The 'gui' subcommand was removed when vendored: its module needs PySide6,\n"
        "# an optional upstream extra Cratekit does not install, so the command could\n"
        "# only ever raise.\n"
    )
    return text[:start] + replacement + text[end + 1 :]


def read_version(unpacked: Path) -> str:
    """Read the version from the sdist's own PKG-INFO, never from a renamable filename."""
    pkg_info = unpacked / "PKG-INFO"
    if pkg_info.is_file():
        for line in pkg_info.read_text(encoding="utf-8").splitlines():
            if line.startswith("Version:"):
                return line.split(":", 1)[1].strip()
    raise SystemExit(
        f"{unpacked.name} carries no PKG-INFO Version field; refusing to guess a version"
    )


def extract_sdist(archive: Path, into: Path) -> Path:
    """Unpack the sdist and return the directory holding its package."""
    with tarfile.open(archive, "r:gz") as tar:
        # filter="data" refuses absolute paths, parent traversal and device nodes.
        tar.extractall(into, filter="data")
    candidates = [p for p in into.iterdir() if p.is_dir()]
    if len(candidates) != 1:
        raise SystemExit(f"expected one top-level directory in {archive.name}, got {candidates}")
    return candidates[0]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("sdist", type=Path, help="upstream tidal_dl_ng-<version>.tar.gz")
    args = parser.parse_args(argv[1:])

    if not args.sdist.is_file():
        raise SystemExit(f"no such file: {args.sdist}")

    with tempfile.TemporaryDirectory() as scratch:
        unpacked = extract_sdist(args.sdist, Path(scratch))
        version = read_version(unpacked)
        source_package = unpacked / UPSTREAM_PACKAGE
        license_file = unpacked / "LICENSE"
        if not source_package.is_dir():
            raise SystemExit(f"{args.sdist.name} has no {UPSTREAM_PACKAGE}/ package")
        if not license_file.is_file() or not license_file.read_text().strip():
            raise SystemExit(
                f"{args.sdist.name} carries no non-empty LICENSE. KTD19 requires the "
                f"vendored component's own licence text to ship; refusing to vendor."
            )

        if VENDOR_PACKAGE.exists():
            shutil.rmtree(VENDOR_PACKAGE)
        shutil.copytree(source_package, VENDOR_PACKAGE)

        for relative in (*DROP_GUI, *DROP_CREDENTIAL_CARRIERS):
            target = VENDOR_PACKAGE / relative
            if not target.exists():
                raise SystemExit(
                    f"expected to drop {relative}, but it is not in {args.sdist.name}. "
                    f"Upstream moved; re-derive the reduction list before vendoring."
                )
            shutil.rmtree(target) if target.is_dir() else target.unlink()

        # Compiled artifacts and editor droppings, if the sdist ever carries them.
        for junk in list(VENDOR_PACKAGE.rglob("__pycache__")):
            shutil.rmtree(junk, ignore_errors=True)
        for junk in list(VENDOR_PACKAGE.rglob("*.py[co]")):
            junk.unlink()

        for patch in (
            PATCH_ATMOS_CREDENTIALS,
            PATCH_ATMOS_ID,
            PATCH_ATMOS_SECRET,
            PATCH_COMMENTED_CLIENT_ID,
            PATCH_COMMENTED_CLIENT_SECRET,
            PATCH_DISPLAY_NAME,
            PATCH_STATE_DIRECTORY_ADOPTION,
            _pinned_metadata_patch(version),
            PATCH_DROP_TOML_IMPORT,
            PATCH_DROP_PATH_IMPORT,
            PATCH_R17_VORBIS,
            PATCH_R17_ID3,
            PATCH_R17_MP4,
            PATCH_R17_SOURCE,
            PATCH_PKCE_TOKEN_FIELD,
            PATCH_PKCE_TOKEN_PERSIST,
            PATCH_PKCE_LOGIN_REUSE,
            PATCH_PKCE_LOGIN_MINT,
        ):
            patch.apply(VENDOR_PACKAGE)

        cli = VENDOR_PACKAGE / "cli.py"
        cli.write_text(strip_gui_entry_point(cli.read_text(encoding="utf-8")), encoding="utf-8")

        for module in sorted(VENDOR_PACKAGE.rglob("*.py")):
            module.write_text(
                rewrite_internal_imports(module.read_text(encoding="utf-8")), encoding="utf-8"
            )

        # The licence ships inside the package and again under vendor/; a test
        # holds the two byte identical.
        shutil.copyfile(license_file, VENDOR_PACKAGE / "LICENSE")
        VENDOR_LICENSE_COPY.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(license_file, VENDOR_LICENSE_COPY)

    print(f"vendored {UPSTREAM_PACKAGE} {version} into {VENDOR_PACKAGE.relative_to(REPO_ROOT)}")
    print("next: update VENDORED in src/cratekit/_vendor/__init__.py, then run")
    print("  python scripts/scan_repo.py && python -m pytest tests/test_vendor_import.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
