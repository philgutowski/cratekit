"""Third-party code copied into the repository because no index still serves it.

KTD4. The acquisition layer's downloader was removed from GitHub and from PyPI in
December 2025, together with its author's account. Its documented install command
fails outright, so a friend cloning Cratekit cannot provision the tool from
anywhere. A committed source tree is the only shape that survives ``git clone``,
an editable install, and Windows. A ``file://`` dependency reference does none of
those: it is not portable across installers and it breaks under ``uv``.

**Nothing here is expressed as a dependency specifier.** That is the load-bearing
half of the decision, and ``tests/test_vendor_import.py`` asserts it. The moment
the vendored project's name appears in ``pyproject.toml``, an install starts
asking an index for a package the index deleted, and the failure surfaces as a
resolution error on somebody else's machine rather than as a decision here.

Transitive dependencies that DO remain on PyPI stay ordinary dependencies. They
are declared in ``pyproject.toml`` with the upper bounds their upstream declared,
because vendoring moved the responsibility for those bounds onto Cratekit: no
resolver reads the vendored package's own metadata any more.

**This package is not an adapter.** It is the raw tree. The typed contract that
makes the downloader replaceable is U14's ``cratekit.acquire``, and nothing
outside that module should import from here.

``vendor/README.md`` records the full inventory, the licence of each component,
what was removed and patched and why, and the procedure for replacing it.
``scripts/revendor_downloader.py`` executes that procedure and refuses to run if
any patch no longer applies.
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple


class VendoredComponent(NamedTuple):
    """Provenance for one vendored tree.

    Recorded as data rather than as prose so ``crate doctor`` can report exactly
    which copy is installed, and so a test can assert the declared version still
    matches the code on disk. A version recorded only in a README is a version
    that goes stale silently, and "which copy do you have" is the first question
    asked about a package whose upstream no longer exists to check against.
    """

    project: str
    """Upstream distribution name, as it was published while it still existed."""

    version: str
    """The vendored release. Must equal the tree's own ``__version__``."""

    license_id: str
    """SPDX identifier declared by the upstream distribution metadata."""

    license_path: str
    """Licence text location, relative to this package."""

    repository: str
    """Upstream repository. Unreachable since December 2025; kept for attribution."""

    vendored_on: str
    """ISO date this copy was extracted, so staleness is measurable."""

    reason: str
    """Why this is vendored rather than depended on."""


DOWNLOADER = VendoredComponent(
    project="tidal-dl-ng",
    version="0.33.0",
    license_id="AGPL-3.0-only",
    license_path="downloader/LICENSE",
    repository="https://github.com/exislow/tidal-dl-ng",
    vendored_on="2026-08-01",
    reason=(
        "removed from GitHub and PyPI in December 2025 along with its author's "
        "account; no public index still serves it, so a fresh install cannot "
        "acquire it (R6, R8)"
    ),
)

VENDORED: tuple[VendoredComponent, ...] = (DOWNLOADER,)


def license_text(component: VendoredComponent) -> str:
    """Return the licence text shipped alongside ``component``.

    KTD19 keeps authored Cratekit code under MIT while each vendored component
    keeps its own licence. Reading the text through here rather than through a
    hardcoded path is what lets the packaging test assert the file is genuinely
    present in an INSTALLED wheel, not merely in the source checkout, which is
    the case where a missing ``package-data`` entry would otherwise go unnoticed.
    """
    return (Path(__file__).parent / component.license_path).read_text(encoding="utf-8")
