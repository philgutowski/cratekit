"""The volume gates: the library's own volume, and every mapped rule's (U27).

Part of :mod:`cratekit.core.session`, which re-exports every name here; read them there. A
name of the session outside this file, and every seam a test patches, is read through
``session`` at call time so a patch on the session bites here too (U300).
"""

from __future__ import annotations

from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from cratekit.core import config, locations, preflight
from cratekit.core.call_time import session as _session
from cratekit.core.cause import (
    Scope,
    refuse,
)
from cratekit.core.exit_codes import Remedy

#: Which refusal slug each mount verdict raises, a table so a new mount state
#: with no entry fails a test rather than falling to a default.
_MOUNT_REASONS: Mapping[preflight.MountState, str] = MappingProxyType(
    {
        preflight.MountState.NOT_MOUNTED: "library-volume-unmounted",
        preflight.MountState.LIBRARY_PATH_MISSING: "library-volume-unmounted",
        preflight.MountState.MOUNTED_ELSEWHERE: "library-volume-mismatch",
        preflight.MountState.FOREIGN_VOLUME: "library-volume-mismatch",
        preflight.MountState.IDENTITY_UNAVAILABLE: "library-volume-mismatch",
        preflight.MountState.IDENTITY_NOT_RECORDED: "library-volume-mismatch",
    }
)


def assert_volume_identity(
    cfg: config.Config,
    *,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> preflight.MountStatus:
    """Refuse unless the configured path holds the volume this library was set up on.

    At destructive strength, so an unreadable identity is fatal. The
    precondition error is converted here so one condition has one identity.
    """
    try:
        return preflight.assert_library_volume(
            cfg.library.root,
            cfg.library.volume_id,
            destructive=True,
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
        )
    except preflight.LibraryVolumeError as exc:
        reason = _MOUNT_REASONS.get(exc.status.state, "library-volume-mismatch")
        raise refuse(
            reason,
            f"{exc.detail}, so this destructive session refuses before it "
            f"resolves a single path",
            remedy=Remedy.MOUNT_LIBRARY_VOLUME,
            scope=Scope.RUN,
            detail={
                "state": str(exc.status.state),
                "configured_root": str(exc.status.configured_root),
                "recorded_identity": exc.status.recorded_identity,
                "observed_identity": exc.status.observed_identity,
            },
        ) from exc


#: Which refusal slug each mount verdict raises for a prefix rule target, apart
#: from ``_MOUNT_REASONS`` since those slugs carry the library volume's remedy.
_MAPPED_REASONS: Mapping[preflight.MountState, str] = MappingProxyType(
    {
        preflight.MountState.NOT_MOUNTED: "mapped-volume-unmounted",
        preflight.MountState.MOUNTED_ELSEWHERE: "mapped-volume-mismatch",
        preflight.MountState.FOREIGN_VOLUME: "mapped-volume-mismatch",
        preflight.MountState.IDENTITY_UNAVAILABLE: "mapped-volume-mismatch",
        preflight.MountState.IDENTITY_NOT_RECORDED: "mapped-volume-mismatch",
    }
)

#: The verdicts under which a rule's target HAS proved its identity, so the two
#: tables are total over the enum. ``LIBRARY_PATH_MISSING`` means the identity
#: matched; a missing directory is refused per row, only when a row uses it.
_MAPPED_PROVED: frozenset[preflight.MountState] = frozenset(
    {preflight.MountState.OK, preflight.MountState.LIBRARY_PATH_MISSING}
)


def expected_rule_identity(cfg: config.Config, rule: locations.PrefixRule) -> str | None:
    """The identity a rule's target must show, or None when nothing says.

    A rule's own identity first; a target inside the library root (lexically,
    by the resolver's test) is held to the library's. Anything else is None,
    never the library's, since an ejected drive's leftover directory on the
    boot disk would match it.
    """
    if rule.volume_id:
        return rule.volume_id
    inside = locations.resolve_recorded_path(rule.target or "/", root=cfg.library.root)
    if inside.resolution is locations.Resolution.UNDER_ROOT:
        return cfg.library.volume_id
    return None


#: The path crosses a place this platform mounts volumes and nothing is mounted there.
_EMPTY_MOUNT_SLOT = "mount_slot_empty"
_UNREACHABLE = "unreachable"


def _held_to(rule: locations.PrefixRule) -> str:
    """Whose identity the comparison used, since a rule inside the root records none."""
    if rule.volume_id:
        return "the volume recorded on that rule"
    return "the library's volume, which a target inside the library root is held to"


def _mapped_steps(
    key: str,
    rule: locations.PrefixRule,
    probe: str,
    status: preflight.MountStatus,
    observed: str | None,
) -> tuple[str, ...]:
    """What a person does about one rule. One act, naming the rule and the disk."""
    state = status.state
    if state is preflight.MountState.IDENTITY_NOT_RECORDED:
        if observed:
            return (
                f"the volume at {probe} identifies as {observed} now; confirm that "
                f"is the disk those tracks live on, then record it as volume_id on "
                f"{key}",
            )
        return (
            f"with the right disk mounted at {probe}, record its identity as "
            f"volume_id on {key}",
        )
    if state is preflight.MountState.NOT_MOUNTED:
        return (f"mount the volume {key} points at, or correct that rule's 'to' ({probe})",)
    if state is preflight.MountState.MOUNTED_ELSEWHERE:
        return (
            f"that volume is mounted at {status.found_at}; mount it at {probe}, or "
            f"correct the 'to' of {key}",
        )
    if state is preflight.MountState.FOREIGN_VOLUME:
        if rule.volume_id and observed:
            return (
                f"mount the volume recorded on {key} at {probe}, or, if the volume "
                f"there now ({observed}) is the right one, record it as that "
                f"rule's volume_id",
            )
        return (f"mount the right volume at {probe}, or correct the 'to' of {key}",)
    return (
        f"no identity can be read for the filesystem {probe} sits on, so nothing "
        f"can prove which disk {key} reaches; move those tracks under the library "
        f"root or remove the rule",
    )


def _mapped_problem(rule: locations.PrefixRule, status: preflight.MountStatus) -> str:
    """One clause on what was observed at a rule's target. No verb for the person."""
    state = status.state
    if state is preflight.MountState.IDENTITY_NOT_RECORDED:
        return (
            "that target is not under the library root as configuration spells "
            "it and the rule records no volume identity, so nothing proves which "
            "disk it reaches"
        )
    if state is preflight.MountState.NOT_MOUNTED:
        return f"{_held_to(rule)} is not mounted"
    if state is preflight.MountState.MOUNTED_ELSEWHERE:
        return f"{_held_to(rule)} is mounted at {status.found_at} instead"
    if state is preflight.MountState.FOREIGN_VOLUME:
        return (
            f"a different volume is there than {_held_to(rule)}: expected identity "
            f"{status.recorded_identity}, mounted identity {status.observed_identity}"
        )
    return f"no volume identity is readable for the filesystem at {status.mount_point}"


def _assert_rule_volume(
    cfg: config.Config,
    index: int,
    rule: locations.PrefixRule,
    probe: Path,
    *,
    identity_provider: preflight.IdentityProvider | None,
    mount_enumerator: preflight.MountEnumerator | None,
) -> preflight.MountStatus:
    """Prove ``probe``, a path reached through rule ``index``, is on that rule's volume.

    An empty mount slot is an unattached drive whatever identity a walk upward
    finds, so ``preflight.identity_source`` is asked before any identity.
    """
    key = f"library.location_prefix_map[{index}]"
    target = rule.target or "/"
    detail: dict[str, Any] = {
        "rule": index,
        "source": rule.source,
        "target": target,
        "probed": str(probe),
    }
    opening = f"prefix rule {index} maps {rule.source} onto {target}, and "
    closing = ", so this destructive session refuses rather than follow that rule"
    identity_of = identity_provider or preflight.default_identity_provider()
    try:
        source = preflight.identity_source(probe)
        if source is None:
            raise refuse(
                "mapped-volume-unmounted",
                f"{opening}{probe} is where a volume mounts and nothing is "
                f"mounted there now{closing}",
                steps=(f"mount the volume {key} points at, or correct that rule's 'to'",),
                scope=Scope.RUN,
                detail={**detail, "state": _EMPTY_MOUNT_SLOT},
            )
        try:
            return preflight.assert_library_volume(
                probe,
                expected_rule_identity(cfg, rule),
                destructive=True,
                identity_provider=identity_provider,
                mount_enumerator=mount_enumerator,
            )
        except preflight.LibraryVolumeError as exc:
            status = exc.status
            if status.state in _MAPPED_PROVED:
                return status
            # Indexed, no default: an undecided verdict must fail.
            reason = _session()._MAPPED_REASONS[status.state]
            observed = status.observed_identity
            if status.state is preflight.MountState.IDENTITY_NOT_RECORDED:
                # Read from the accepted mount, so the step can name the identity.
                observed = identity_of(source)
            raise refuse(
                reason,
                f"{opening}{_mapped_problem(rule, status)}{closing}",
                steps=_mapped_steps(key, rule, str(probe), status, observed),
                scope=Scope.RUN,
                detail={
                    **detail,
                    "state": str(status.state),
                    "recorded_identity": status.recorded_identity,
                    "observed_identity": observed,
                },
            ) from exc
    except OSError as exc:
        # Could not look is its own refusal, not an internal defect.
        raise refuse(

            "mapped-volume-mismatch",
            f"{opening}which volume {probe} sits on could not be established "
            f"({exc}){closing}",
            steps=(
                f"make the way to {probe} readable by this account, or correct "
                f"the 'to' of {key}",
            ),
            scope=Scope.RUN,
            detail={**detail, "state": _UNREACHABLE},
        ) from exc


def assert_mapped_volume_identities(
    cfg: config.Config,
    rules: Sequence[locations.PrefixRule],
    *,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> tuple[preflight.MountStatus, ...]:
    """Refuse unless every prefix rule's target sits on the volume it was recorded on.

    A pass following a rule writes off the library root, often onto the archive
    disk. Every rule is asked, since knowing which a row uses means resolving
    paths first. A present directory is not an identity.
    """
    return tuple(
        _assert_rule_volume(
            cfg,
            index,
            rule,
            Path(rule.target or "/"),
            identity_provider=identity_provider,
            mount_enumerator=mount_enumerator,
        )
        for index, rule in enumerate(rules)
    )


def assert_mapped_file_volume(
    cfg: config.Config,
    rules: Sequence[locations.PrefixRule],
    index: int,
    path: Path | str,
    *,
    identity_provider: preflight.IdentityProvider | None = None,
    mount_enumerator: preflight.MountEnumerator | None = None,
) -> preflight.MountStatus:
    """Prove the volume ONE FILE reached through rule ``index`` actually sits on.

    The file's own directory is probed, since a nested mount or symlink can sit
    between it and the target, and per file, since a drive can be swapped
    during a long pass.
    """
    return _assert_rule_volume(
        cfg,
        index,
        rules[index],
        Path(path).parent,
        identity_provider=identity_provider,
        mount_enumerator=mount_enumerator,
    )
