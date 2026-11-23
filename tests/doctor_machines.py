"""The two synthetic machines a doctor drive is measured against.

Shared by ``tests/test_doctor.py``, which breaks one seam at a time, and
``tests/test_cli_contract.py``, which asserts every declared precondition can
answer AND refuse, the assertion that keeps conformance 8 from being a
tautology. The green baseline answers every seam, so a test names only the
seam it breaks and never depends on the real machine; the hostile one breaks
everything, which a stub doctor emitting empty findings cannot survive.

The class is captured at IMPORT, so a test replacing ``doctor.Probes`` does
not replace what these build machines with.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from cratekit.cli.doctor import InstallOrigin as _InstallOrigin
from cratekit.cli.doctor import Probes as _Probes
from cratekit.deletion.trash import TrashLayout, TrashStatus
from cratekit.write.metadata_cli import ResolutionTotals

#: A synthetic volume identity. Shaped like a real one and belonging to nobody,
#: because R1 forbids a shipped artifact from carrying a real library string.
VOLUME = "F1E2-D3C4"

#: The application version both machines agree is installed, so a pin recorded in
#: a fixture matches on the green machine and the drift is deliberate elsewhere.
INSTALLED_APP_VERSION = "7.0.1"


def _usable_trash(path: Path) -> TrashStatus:
    """A volume whose Trash accepts a move, derived from the path the check was handed."""
    root = Path(path) / ".Trashes"
    return TrashStatus(TrashLayout(root=root, files=root / "501"), True)


def _absent_trash(path: Path) -> TrashStatus:
    """A volume nobody has ever deleted from, which is not a fault but the common case.

    The Trash is created on first use, and doctor asks with ``create=False``.
    """
    root = Path(path) / ".Trashes"
    return TrashStatus(
        TrashLayout(root=root, files=root / "501"),
        False,
        f"{root / '501'} is not a directory",
        absent=True,
    )


def _no_trash(path: Path) -> TrashStatus:
    """A volume with no usable Trash: UNWRITABLE, the one shape no create can fix."""
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
        # A collection whose every row resolves, described rather than built.
        path_survey=lambda _cfg: ResolutionTotals(active=10, unresolved=0, unmapped=0),
        # A release install that is current, so no green run reaches the
        # network and none depends on how the suite's own copy was installed.
        install_origin=lambda: _InstallOrigin(
            kind="vcs", version="0.1.0", url="https://github.com/philgutowski/cratekit"
        ),
        release_tags=lambda _url: ("v0.1.0",),
        # U185. No DEADCA7 on the green machine, so no run reads this account's
        # own support folder, nor (U224) its Applications or state folders.
        deadca7_home=lambda: None,
        deadca7_installed=lambda: (),
        # U181. A copy whose vocal model can score, so no green run imports
        # torch, and a library never scored, so no upgrade adds an extra.
        vocal_requirement=lambda: None,
        vocals_scored=lambda _cfg: False,
    )
    defaults.update(overrides)
    return _Probes(**defaults)


def hostile(**overrides) -> _Probes:
    """A machine on which every precondition a verb can declare is broken.

    One machine, so a do-nothing doctor answers it exactly as the green one. The
    identity is a DIFFERENT one rather than absent, so the mount resolves to a
    foreign volume, a refusal, not a platform note.
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
        # The library R-372 was found on: every row under a drive name no rule maps.
        path_survey=lambda _cfg: ResolutionTotals(
            active=10, unresolved=10, unmapped=10, prefixes={"/renamed/DRIVE": 10}
        ),
        # U181. The copy sitting 51 landed from: no vocals extra.
        vocal_requirement=lambda: ("extra", "the 'vocals' extra is not installed here"),
    )
    defaults.update(overrides)
    return green(**defaults)
