#!/usr/bin/env python3
"""Rebuild ``src/cratekit/_vendor/tidal_dl_ng/`` from an upstream source distribution.

KTD4 vendors the downloader as a source tree because its upstream was removed
from GitHub and PyPI in December 2025, taking the author's account with it. There
is no index to install it from, so a committed tree is the only thing that lets a
friend's clone acquire music at all.

WHY THIS IS A SCRIPT AND NOT A PARAGRAPH IN A README.

Vendoring with patches has one classic failure: somebody bumps the vendored
version, re-copies the tree, and silently drops the patches. The tree still
imports, the tests still pass, and the thing the patches prevented comes back.
Here the patches are declared as exact expected text. A patch whose anchor is
missing ABORTS the re-vendor rather than being skipped, so a drop is loud at the
moment it happens instead of quiet until it matters.

The three reductions and three patches below each exist for a failure that was
observed in the 0.33.0 artifact, not for tidiness. Each carries the failure in
its own comment.

Usage::

    python scripts/revendor_downloader.py path/to/tidal_dl_ng-<version>.tar.gz

The upstream artifact is deliberately NOT committed. It is a third-party sdist,
it is large, and committing it would put a second copy of the vendored code in
the repository where nothing checks it. ``vendor/README.md`` records where the
known-good copies live.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VENDOR_PACKAGE = REPO_ROOT / "src" / "cratekit" / "_vendor" / "tidal_dl_ng"
VENDOR_LICENSE_COPY = REPO_ROOT / "vendor" / "LICENSE.tidal-dl-ng"

UPSTREAM_PACKAGE = "tidal_dl_ng"
VENDORED_IMPORT_ROOT = "cratekit._vendor.tidal_dl_ng"

# ---------------------------------------------------------------------------
# Reduction 1: the GUI half is not vendored.
#
# Every module here imports PySide6 at module scope. PySide6 is an OPTIONAL
# extra upstream ("gui"), so a headless install cannot import any of them —
# verified by importing each one in a clean environment and getting
# ModuleNotFoundError for all five. Vendoring code that provably cannot import
# is not conservatism, it is shipping a trap. It also drags 356 KB of icon
# binaries and two dependencies (ansi2html, coloredlogs) that nothing in the
# retained tree imports.
# ---------------------------------------------------------------------------
DROP_GUI = (
    "gui.py",
    "logger.py",
    "dialog.py",
    "worker.py",
    "helper/gui.py",
    "ui",
)

# ---------------------------------------------------------------------------
# Reduction 2: api.py is not vendored.
#
# Three independent reasons, any one of which is sufficient:
#   1. It carries five hardcoded third-party streaming OAuth client id and
#      client secret pairs in plaintext, harvested from other projects. R1 says
#      no shipped artifact carries credential material.
#   2. It raises JSONDecodeError AT IMPORT in 0.33.0: its embedded JSON blob uses
#      `//` comments, which JSON does not have, and the module parses it at
#      module scope. It is upstream-broken, not merely unused.
#   3. Nothing in the package imports it.
#
# Note for whoever widens the secret scan: the repository scanner does NOT flag
# these, because its credential-assignment pattern expects snake_case
# (`client_secret`) and these are camelCase JSON keys (`"clientSecret":`). The
# scan caught the snake_case pair in config.py and missed all five here.
# ---------------------------------------------------------------------------
DROP_CREDENTIAL_CARRIERS = ("api.py",)


class PatchError(RuntimeError):
    """A declared patch did not find the text it was written against."""


class Patch:
    """One exact text substitution, with the failure it prevents recorded.

    ``old`` must appear EXACTLY ONCE. Not zero times, which means upstream moved
    and the patch is now a no-op nobody noticed. Not twice, which means the
    anchor stopped being specific enough to say which site is being changed.
    """

    def __init__(self, relative_path: str, old: str, new: str, why: str) -> None:
        self.relative_path = relative_path
        self.old = old
        self.new = new
        self.why = why

    def apply(self, root: Path) -> None:
        target = root / self.relative_path
        if not target.is_file():
            raise PatchError(f"{self.relative_path} is not in the extracted tree; {self.why}")
        text = target.read_text(encoding="utf-8")
        count = text.count(self.old)
        if count != 1:
            raise PatchError(
                f"{self.relative_path}: expected exactly 1 occurrence of the patch "
                f"anchor, found {count}. Upstream changed under this patch. "
                f"Re-derive it by hand; do NOT skip it. The patch exists because: {self.why}"
            )
        target.write_text(text.replace(self.old, self.new), encoding="utf-8")


class LinePatch:
    """Replace a WHOLE line, matched by its leading text.

    Every credential removal below has to be a line patch rather than a
    substitution, and the reason is worth stating because getting it wrong is
    silent. A substitution anchored on ``ATMOS_ID_B64 = `` replaces only that
    prefix and leaves the literal that follows it sitting in the file under a new
    name. The credential would still ship, the diff would look like a removal,
    and every test asserting the constant is empty would still pass.

    Matching by prefix and discarding the rest of the line is also what keeps the
    secrets out of THIS file: the script never has to name a value to delete it.
    """

    def __init__(self, relative_path: str, prefix: str, replacement: str, why: str) -> None:
        self.relative_path = relative_path
        self.prefix = prefix
        self.replacement = replacement
        self.why = why

    def apply(self, root: Path) -> None:
        target = root / self.relative_path
        if not target.is_file():
            raise PatchError(f"{self.relative_path} is not in the extracted tree; {self.why}")
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


class SpanPatch:
    """Replace everything from one anchor up to the next, exclusive.

    Used where a whole function body has to go. Anchoring on the function's first
    line and on the line that follows it keeps the anchors short and stable,
    where pasting the entire original body as the anchor would break on any
    whitespace change upstream and give no clue which change did it.

    Both anchors must occur exactly once, for the same reason ``Patch`` requires
    it: an anchor that matches twice no longer says which span is meant.
    """

    def __init__(
        self, relative_path: str, start: str, end: str, replacement: str, why: str
    ) -> None:
        self.relative_path = relative_path
        self.start = start
        self.end = end
        self.replacement = replacement
        self.why = why

    def apply(self, root: Path) -> None:
        target = root / self.relative_path
        if not target.is_file():
            raise PatchError(f"{self.relative_path} is not in the extracted tree; {self.why}")
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


# ---------------------------------------------------------------------------
# Patch 1: the Dolby Atmos client credentials are emptied.
#
# Upstream base64-encodes them and splits the literal across string
# concatenations, which reads as a deliberate attempt to get past exactly the
# kind of scan this repository runs. Decoded, one of them is the same key
# published in api.py. Shipping them is an R1 violation whether or not a scanner
# happens to catch the encoded form.
#
# Emptying rather than deleting the feature is the smaller, more faithful patch:
# `Tidal.switch_to_atmos_session()` keeps its shape, fails its login, and returns
# False, which `Download._get_stream_info` already handles by logging and
# returning an empty stream record. It can only be reached when the user sets
# `download_dolby_atmos`, which defaults to False and which R21's lossless policy
# forbids anyway: the Atmos path requests Quality.low_320k, a lossy stream.
# ---------------------------------------------------------------------------
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

# Matched by variable name, never by value, so this script never spells the
# secrets it removes. The whole line goes; see LinePatch for why a substitution
# would have shipped them under a different name.
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

# ---------------------------------------------------------------------------
# Patch 2: the commented-out plaintext credential pair in config.py.
#
# Dead code, but a scanner cannot tell a commented credential from a live one
# and neither can a reader skimming a diff. The repository scan flags both lines
# today; leaving them in would force an exemption, and an exemption in the secret
# scan is the hole the widened scan exists to close.
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Patch 3: version detection stops reading whatever pyproject.toml is nearby.
#
# THIS IS THE SHARPEST HAZARD IN THE ARTIFACT and it is caused by vendoring
# itself. Upstream's `metadata_project()` walks up to THREE directories from its
# own __file__ looking for a pyproject.toml, and if it finds one it reads
# `["project"]["version"]` and `["project"]["urls"]["repository"]` out of it,
# with no guard on whose file it just read.
#
# Vendored at src/cratekit/_vendor/tidal_dl_ng/, those three parents are
# tidal_dl_ng/, _vendor/, and cratekit/. Cratekit's own pyproject.toml sits one
# level further up, so today the walk misses it by exactly one directory. If it
# ever reached it, the lookup would raise KeyError — Cratekit declares no
# [project.urls] — and the KeyError is outside the try, so `import tidal_dl_ng`
# would fail at import time for a reason naming none of this.
#
# Depending on a one-level depth coincidence is not a design. The version is
# pinned instead, which also makes `toml` and the importlib.metadata fallback
# unnecessary and removes a dependency.
# ---------------------------------------------------------------------------
def _pinned_metadata_patch(version: str) -> SpanPatch:
    """Replace the whole of ``metadata_project()`` with a pinned constant.

    The upstream body is removed rather than kept for reference. Keeping it would
    keep its ``toml`` and ``pathlib`` imports live, and ``toml`` is an
    unmaintained 2020 package that the standard library replaced with ``tomllib``
    in 3.11. Declaring it as a Cratekit dependency to support dead code is a cost
    with no buyer; the record of what was replaced belongs in vendor/README.md
    and in version control, not in the shipped tree.
    """
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


# The two imports that only the removed body used. Dropping them keeps `toml`
# off Cratekit's dependency list entirely.
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


# ---------------------------------------------------------------------------
# Patch 4: the on-disk application name is pinned.
#
# `__name_display__` is derived from `__package__`, and it is not cosmetic: it
# names the directory holding the settings file, the log, and the persisted
# token (`helper/path.py::path_config_base`). Vendored, `__package__` becomes
# "cratekit._vendor.tidal_dl_ng", and because the distribution is not installed
# under that name `is_dev_env()` appends "-dev", so the tool would write its
# state to a directory literally named after an internal import path.
#
# Pinning it to the upstream display name keeps vendored behaviour identical to
# a normal install, which is the point of vendoring rather than forking. U14 owns
# redirecting this state once the adapter takes ownership of the credential.
# ---------------------------------------------------------------------------
PATCH_DISPLAY_NAME = Patch(
    relative_path="__init__.py",
    old="__name_display__ = name_app()",
    new=(
        "# Cratekit patch: pinned. Derived from __package__ upstream, which vendored\n"
        "# would name the settings, log, and token directory after an import path.\n"
        '__name_display__ = "tidal-dl-ng"'
    ),
    why="the display name is the on-disk state directory, not a label",
)


# ---------------------------------------------------------------------------
# Patch 5: the downloader stops writing tempo tags. This is R17.
#
# Beat grids belong to rekordbox and to nobody else. The vendored downloader
# writes the streaming provider's BPM into every file it saves, in all three
# containers, and rekordbox reads file tags on import. So a downloaded track
# would arrive carrying a grid seed that nothing in Cratekit put there.
#
# Why that is worse than it sounds: a wrong grid is worse than no grid. Tempo
# detection octave-folds, so a provider BPM lands the grid at half or double
# time, and every cue point and every loop the user ever set against that track
# moves with it. Imported gridless, rekordbox derives tempo from the audio, which
# it is good at and which is reversible.
#
# NOTE FOR WHOEVER OWNS tests/test_no_beatgrid_ever.py: its static checker caught
# ONE of these three. It matches an assignment whose subscript key is in
# FORBIDDEN_TAG_KEYS, which finds the Vorbis "BPM" write and misses both of the
# others: the ID3 write is a CALL, `tags.add(TBPM(...))`, not an assignment, and
# the MP4 key is the atom name "tmpo", which is not in FORBIDDEN_TAG_KEYS. Two
# live R17 violations in shipped code would have passed the guard.
# ---------------------------------------------------------------------------
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

# Defence in depth at the single point where the provider's tempo enters. If a
# later upstream version adds a fourth container writer, the value it would write
# is already zero. The static guard covers the write; this covers the source.
PATCH_R17_SOURCE = LinePatch(
    relative_path="download.py",
    prefix="bpm=track.bpm",
    replacement="            bpm=0,  # R17: the provider's tempo never enters a tag (Cratekit patch)\n",
    why="R17: the provider's tempo is never carried into metadata at all",
)


def rewrite_internal_imports(text: str) -> str:
    """Point the package's absolute self-imports at their vendored location.

    The package imports itself absolutely throughout (``from tidal_dl_ng.config
    import Settings``). Moved under ``cratekit._vendor`` those names no longer
    resolve, so every one has to be re-rooted.

    Absolute re-rooting is used rather than relative imports on purpose. A
    relative rewrite depends on each module's depth inside the package, so it is
    three rules instead of one and it gets a file wrong quietly. This way the
    rewrite is a single rule at any depth, it is greppable, and no reader of a
    vendored file can mistake it for first-party code.
    """
    return text.replace(f"from {UPSTREAM_PACKAGE}", f"from {VENDORED_IMPORT_ROOT}")


def strip_gui_entry_point(text: str) -> str:
    """Remove the CLI's ``gui`` subcommand, whose module is not vendored.

    Leaving it would ship a command that raises ModuleNotFoundError naming a file
    that does not exist, which reads as a broken vendoring job rather than as a
    deliberate reduction.
    """
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
    """Read the version from the sdist's own PKG-INFO.

    Not from the filename. A downloaded artifact gets renamed, and a vendored
    tree that reports a version its code is not is worse than one reporting none:
    it is the field a maintainer checks first when deciding whether a reported
    bug is already fixed.
    """
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
        # filter="data" refuses absolute paths, parent traversal, and device
        # nodes. A vendoring step is exactly where an archive of unknown
        # provenance gets unpacked, so it is the wrong place to trust one.
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
            _pinned_metadata_patch(version),
            PATCH_DROP_TOML_IMPORT,
            PATCH_DROP_PATH_IMPORT,
            PATCH_R17_VORBIS,
            PATCH_R17_ID3,
            PATCH_R17_MP4,
            PATCH_R17_SOURCE,
        ):
            patch.apply(VENDOR_PACKAGE)

        cli = VENDOR_PACKAGE / "cli.py"
        cli.write_text(strip_gui_entry_point(cli.read_text(encoding="utf-8")), encoding="utf-8")

        for module in sorted(VENDOR_PACKAGE.rglob("*.py")):
            module.write_text(
                rewrite_internal_imports(module.read_text(encoding="utf-8")), encoding="utf-8"
            )

        # The licence ships INSIDE the package so it can never be separated from
        # the code it covers, and again at the repository root where a reader
        # looking for licences looks. tests/test_vendor_import.py asserts the two
        # stay byte-identical, so the duplication cannot drift.
        shutil.copyfile(license_file, VENDOR_PACKAGE / "LICENSE")
        VENDOR_LICENSE_COPY.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(license_file, VENDOR_LICENSE_COPY)

    print(f"vendored {UPSTREAM_PACKAGE} {version} into {VENDOR_PACKAGE.relative_to(REPO_ROOT)}")
    print("next: update VENDORED in src/cratekit/_vendor/__init__.py, then run")
    print("  python scripts/scan_repo.py && python -m pytest tests/test_vendor_import.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
