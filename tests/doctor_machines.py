"""The two synthetic machines a doctor drive is measured against.

Here rather than in one test module because two suites need the same pair and a
second copy of a baseline is a second machine: ``tests/test_doctor.py`` drives
individual checks against one broken seam at a time, and
``tests/test_cli_contract.py`` asserts that every check a verb declares as a
precondition can actually answer AND actually refuse. The second of those is the
assertion that stops conformance 8 being a tautology, and it needs a machine
where everything is broken, which is exactly the thing a per-check test never
builds.

WHY A GREEN BASELINE RATHER THAN A BARE ``Probes()``. A test that started from
the real machine would pass or fail on whatever happens to be installed on it, so
every seam is answered here and a test names only the seam it breaks.

WHY THE HOSTILE ONE EXISTS. "A check that cannot fail is not a check" is this
product's own sentence, written in the module these drive. A stub doctor emitting
one empty finding per key satisfies "every declared key comes back with an
answer" while doing no work at all; it cannot satisfy "every declared key refuses
on a machine where that precondition is broken".

The class is captured at IMPORT time on purpose. A test that replaces
``doctor.Probes`` to feed a synthetic machine through the real dispatcher must
not thereby replace the thing these functions call to build one.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from cratekit.cli.doctor import Probes as _Probes
from cratekit.deletion.trash import TrashLayout, TrashStatus

#: A synthetic volume identity. Shaped like a real one and belonging to nobody,
#: because R1 forbids a shipped artifact from carrying a real library string.
VOLUME = "F1E2-D3C4"

#: The application version both machines agree is installed, so a pin recorded in
#: a fixture matches on the green machine and the drift is deliberate elsewhere.
INSTALLED_APP_VERSION = "7.0.1"


def _usable_trash(path: Path) -> TrashStatus:
    """A volume whose Trash accepts a move, described rather than created.

    The layout is derived from the path the check was handed, so a finding built
    from it names the library under test rather than a constant that would be the
    same sentence on every machine.
    """
    root = Path(path) / ".Trashes"
    return TrashStatus(TrashLayout(root=root, files=root / "501"), True)


def _absent_trash(path: Path) -> TrashStatus:
    """A volume nobody has ever deleted from, which is not a fault.

    The per-volume Trash is created on first use by the desktop and by this
    product's own deletion pass, so a fresh volume legitimately has no directory.
    Doctor asks with ``create=False`` and therefore MEETS this state on every
    machine that has not deleted anything yet, which makes it the common case
    rather than an exotic one.
    """
    root = Path(path) / ".Trashes"
    return TrashStatus(
        TrashLayout(root=root, files=root / "501"),
        False,
        f"{root / '501'} is not a directory",
        absent=True,
    )


def _no_trash(path: Path) -> TrashStatus:
    """A volume with no usable Trash, and a problem sentence a finding can carry.

    UNWRITABLE rather than absent, deliberately. An absent directory is the case
    the real probe would create its way out of if anything ever passed
    ``create=True``, so the broken machine describes the one shape no create can
    fix, which is the shape a person actually meets on a read-only mount.
    """
    root = Path(path) / ".Trashes"
    return TrashStatus(
        TrashLayout(root=root, files=root / "501"),
        False,
        f"{root / '501'} is not writable by this account",
    )


def green(**overrides) -> _Probes:
    """A machine on which every check passes, minus whatever a caller breaks."""
    defaults = dict(
        now=datetime(2026, 8, 2, tzinfo=timezone.utc),
        python_version=(3, 12, 4),
        requires_python=">=3.12,<3.14",
        find_binary=lambda name: f"/opt/probe/bin/{name}",
        binary_override_problem=lambda _name: None,
        identity_provider=lambda _path: VOLUME,
        mount_enumerator=lambda: (),
        process_lister=lambda: (),
        keychain_available=lambda: True,
        credential_recorded=lambda _name: True,
        environment_credential=lambda _name: None,
        installed_app_version=lambda _cfg: INSTALLED_APP_VERSION,
        binding_pin_problem=lambda _cfg: None,
        rclone_remotes=lambda _rclone: {},
        checkout_root=lambda: None,
        trash_probe=_usable_trash,
    )
    defaults.update(overrides)
    return _Probes(**defaults)


def hostile(**overrides) -> _Probes:
    """A machine on which every precondition a verb can declare is broken.

    One machine rather than one per key, because the point is what a single run
    reports: a doctor that does no work answers this machine exactly as it
    answers the green one, and the difference between the two reports is the
    evidence that each check observed something.

    The identity is a DIFFERENT one rather than absent, so the mount resolves to
    a foreign volume, which is a refusal, rather than to "no identity available",
    which is a platform note.
    """
    defaults = dict(
        python_version=(3, 11, 0),
        find_binary=lambda _name: None,
        binary_override_problem=lambda _name: None,
        identity_provider=lambda _path: "0000-0000",
        mount_enumerator=lambda: (),
        process_lister=lambda: ("rekordbox",),
        keychain_available=lambda: False,
        credential_recorded=lambda _name: False,
        environment_credential=lambda _name: None,
        installed_app_version=lambda _cfg: INSTALLED_APP_VERSION,
        binding_pin_problem=lambda _cfg: "the recorded pyrekordbox pin is not satisfied",
        rclone_remotes=lambda _rclone: None,
        checkout_root=lambda: None,
        trash_probe=_no_trash,
    )
    defaults.update(overrides)
    return green(**defaults)
