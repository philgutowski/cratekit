"""Doctor's checks of the backups: their ages, the acknowledgment, the comparisons and the remote.

The age checks are INFO in every readable state and FAIL only where a record
cannot be trusted, since a backup that is due is not a fault.
"""

from __future__ import annotations

import os
import stat
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import MappingProxyType

from cratekit.cli.doctor_library import _library_state_unreadable
from cratekit.cli.doctor_model import Finding, Probes, Status, _Inputs, _unchecked
from cratekit.core import (
    backup_facts,
    session,
)
from cratekit.core.cause import (
    CratekitError,
)
from cratekit.core.exit_codes import Remedy


def _whole_days(age: timedelta | None) -> int:
    """An age in whole days, never below zero, for a clock slightly ahead."""
    return max(age.days, 0) if age is not None else 0


def _unreadable_facts(key: str, title: str, exc) -> Finding:
    """The one finding every check reading the backup fact file gives for that."""
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=str(exc),
        remedy=Remedy(str(exc.remedy)),
    )


def _check_backup_portion(key: str, inputs: _Inputs) -> Finding:
    portion = backup_facts.PORTIONS[key.split(".")[-1]]
    title = f"backup age, {portion} portion"
    if inputs.cfg is None:
        return _unchecked(key, title)
    try:
        ages = backup_facts.ages(inputs.cfg, now=inputs.probes.now)
    except backup_facts.BackupFactsUnreadable as exc:
        return _unreadable_facts(key, title, exc)
    answer = next(entry for entry in ages if entry.portion is portion)
    if answer.state is backup_facts.AgeState.NEVER_RECORDED:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                "no completion has been recorded for this portion here, which is "
                "the state of every library before a backup has run once"
            ),
        )
    if answer.state is backup_facts.AgeState.RECORDED_IN_THE_FUTURE:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the recorded completion at {answer.completed_at} is ahead of now. "
                f"Any check comparing an age against a maximum reads a negative age "
                f"as the freshest possible value, so this record silently satisfies "
                f"every freshness test it was written to fail"
            ),
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )
    days = _whole_days(answer.age)
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=(
            f"last completed {days} days ago, to "
            f"{answer.destination or 'an unnamed destination'}{_by_kind(answer)}"
        ),
    )


def _by_kind(answer) -> str:
    """Which kind of run completed a portion and what it changed (U317), or nothing.

    Nothing for an older fact that recorded no kind.
    """
    summary = answer.summary or {}
    took = backup_facts.took(summary.get("seconds"))
    if answer.kind == backup_facts.KIND_QUICK:
        found = ", ".join(
            f"{summary.get(name, 0)} {name}"
            for name in ("added", "changed", "rewritten", "removed")
        )
        return f", by a quick run that sent only what changed ({found}){took}"
    words = {
        backup_facts.KIND_FULL: "by a full check of the whole remote",
        backup_facts.KIND_SKIPPED: "by a skip, since nothing had changed",
        backup_facts.KIND_SNAPSHOT: "by a new dated snapshot",
        backup_facts.KIND_UNCHANGED: "unchanged since its last snapshot, so none was taken",
    }
    said = words.get(answer.kind or "")
    return f", {said}{took}" if said else ""


def _check_backup_acknowledgment(inputs: _Inputs) -> Finding:
    """The backup acknowledgment's window, beside the two ages it was minted over (U184).

    INFO when absent, valid or expired, since a destructive verb's own gate asks
    for one; FAIL only for a record that cannot be understood, since every
    destructive verb refuses on it. Never read off an absent volume, where no
    file would not mean none on record.
    """
    key, title = "backup.acknowledgment", "backup acknowledgment"
    if inputs.cfg is None:
        return _unchecked(key, title)
    unreadable = _library_state_unreadable(inputs, "the backup acknowledgment")
    if unreadable is not None:
        return Finding(key=key, title=title, status=Status.INFO, detail=unreadable)
    try:
        recorded = session.read_acknowledgment(inputs.cfg)
    except CratekitError as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"{exc.cause.message}. Every destructive verb refuses while the "
                f"record reads this way"
            ),
            remedy=exc.cause.remediation.remedy,
        )
    if recorded is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                "none on record; a destructive verb asks for one, minted with "
                "crate session ack"
            ),
        )
    now = inputs.probes.now
    expires = recorded.expires_at.replace(microsecond=0).isoformat()
    if not recorded.valid_at(now):
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"expired at {expires}; a destructive verb asks for a new one, "
                f"minted with crate session ack"
            ),
        )
    left = recorded.expires_at - now
    hours, minutes = divmod(int(left.total_seconds()) // 60, 60)
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=(
            f"valid until {expires}, {hours}h {minutes:02d}m from now, minted by "
            f"the {recorded.rule} rule"
        ),
    )


#: How old the last full comparison may be before the check says to run one.
#: Never a failure, since both modes compare every file.
FULL_COMPARISON_DUE_DAYS = 30


def _check_full_comparison(inputs: _Inputs) -> Finding:
    """How long ago the file mirror last compared folder by folder (R-757).

    Said so the recursive listing the ordinary backup relies on does not go
    unchecked for ever.
    """
    key, title = "backup.full_comparison", "backup, last full comparison"
    if inputs.cfg is None:
        return _unchecked(key, title)
    try:
        answer = backup_facts.full_comparison_age(inputs.cfg, now=inputs.probes.now)
    except backup_facts.BackupFactsUnreadable as exc:
        return _unreadable_facts(key, title, exc)
    run_one = "Run one with: crate backup run --full"
    if answer.state is backup_facts.AgeState.NEVER_RECORDED:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                "no backup here has compared the library with the remote folder "
                "by folder. Every backup compares every file, through one "
                f"recursive listing of the remote. {run_one}"
            ),
        )
    if answer.state is backup_facts.AgeState.RECORDED_IN_THE_FUTURE:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the recorded full comparison at {answer.completed_at} is ahead "
                f"of now, so its age cannot be stated"
            ),
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )
    days = _whole_days(answer.age)
    due = f". {run_one}" if days >= FULL_COMPARISON_DUE_DAYS else ""
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=(
            f"last ran {days} days ago, against "
            f"{answer.destination or 'an unnamed destination'}{due}"
        ),
    )


def _check_full_check(inputs: _Inputs) -> Finding:
    """When the file mirror last ran a full check, and when the next is due (U317).

    A due check is not a fault, since the next ``crate backup run`` runs it.
    """
    key, title = "backup.full_check", "backup, last full check"
    if inputs.cfg is None:
        return _unchecked(key, title)
    try:
        answer = backup_facts.full_check_age(inputs.cfg, now=inputs.probes.now)
    except backup_facts.BackupFactsUnreadable as exc:
        return _unreadable_facts(key, title, exc)
    run_one = "To run one now: crate backup run --check"
    if answer.state is backup_facts.AgeState.NEVER_RECORDED:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                "no full check of the remote is on record, so the next backup "
                f"runs one. {run_one}"
            ),
        )
    if answer.state is backup_facts.AgeState.RECORDED_IN_THE_FUTURE:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the recorded full check at {answer.completed_at} is ahead of "
                f"now, so when the next is due cannot be stated"
            ),
            remedy=Remedy.REPAIR_BACKUP_FACTS,
        )
    due = backup_facts.full_check_due(answer)
    when = (
        "is due now, so the next backup runs one"
        if due is None or due <= inputs.probes.now
        else f"is due {due.date().isoformat()}; until then a backup sends only "
        f"what changed, or is skipped when nothing did"
    )
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=(
            f"last ran {_whole_days(answer.age)} days ago, against "
            f"{answer.destination or 'an unnamed destination'}. The next {when}. "
            f"{run_one}"
        ),
    )


#: The folder inside DEADCA7's support folder where it backs rekordbox's
#: database up before every push, one entry per push (U185).
DEADCA7_BACKUPS = "rekordbox-backups"


def _newest_entry(folder: Path) -> datetime | None:
    """When the newest entry in ``folder`` was written, or None for an empty one."""
    times = [
        entry.stat().st_mtime for entry in folder.iterdir() if not entry.name.startswith(".")
    ]
    if not times:
        return None
    return datetime.fromtimestamp(max(times), tz=timezone.utc)


def _folder_presence(path: Path) -> OSError | bool:
    """Whether ``path`` is a folder here, or the error that kept it from being read (U224).

    Uses ``os.stat``, since ``Path.is_dir`` answers False for a refused stat on
    later Pythons. Not found is absent; any other refusal is unread, never absent.
    """
    try:
        mode = os.stat(path).st_mode
    except (FileNotFoundError, NotADirectoryError):
        return False
    except OSError as exc:
        return exc
    return stat.S_ISDIR(mode)


def _said(exc: BaseException) -> str:
    return f"{type(exc).__name__}: {exc}"


def _deadca7_presence(
    probes: Probes,
) -> tuple[Path | None, bool | None, list[Path], list[str]]:
    """DEADCA7's support folder, whether it is here, the install signals found,
    and every place that could not be read (U224).

    A probe that raises is unread, never absent, and an unread support folder
    answers None. Install signals are asked only without the support folder.
    """
    unread: list[str] = []
    support: bool | None = False
    try:
        home = probes.deadca7_home()
    except Exception as exc:  # noqa: BLE001 - a broken probe is unread, never absent
        home, support = None, None
        unread.append(f"its support folder could not be located ({_said(exc)})")
    if home is not None:
        state = _folder_presence(home)
        if isinstance(state, OSError):
            support = None
            unread.append(f"{home} could not be read ({_said(state)})")
        else:
            support = state
    found: list[Path] = []
    if not support:
        try:
            places = tuple(probes.deadca7_installed())
        except Exception as exc:  # noqa: BLE001 - a broken probe is unread, never absent
            places = ()
            unread.append(f"where its app is installed could not be located ({_said(exc)})")
        for place in places:
            state = _folder_presence(place)
            if isinstance(state, OSError):
                unread.append(f"{place} could not be read ({_said(state)})")
            elif state:
                found.append(place)
    return home, support, found, unread


def _check_deadca7_push(inputs: _Inputs) -> Finding:
    """Whether DEADCA7 is here, when it last pushed into the database, and against what.

    DEADCA7 backs the database up into its own folder before every push, so the
    newest entry's modification time is taken as the last push, unconfirmed
    until a real push is read. INFO in every case: a push newer than the last
    backup is a reason to run one, not a fault. Never launches the app.
    """
    key, title = "deadca7.push", "DEADCA7 pushes into the library"
    if inputs.cfg is None:
        return _unchecked(key, title)
    home, support, found, unread = _deadca7_presence(inputs.probes)

    def said(detail: str) -> Finding:
        return Finding(key=key, title=title, status=Status.INFO, detail=detail)

    # Installed is the support folder or any install signal, since the shipped
    # app may never make the support folder (U224).
    if not support and not found:
        if unread:
            return said("whether DEADCA7 is installed here cannot be said: " + "; ".join(unread))
        return said(
            "DEADCA7 is not installed here, so nothing else writes the library beside rekordbox"
        )
    backups = None if home is None else home / DEADCA7_BACKUPS
    unconfirmed = (
        "Where it backs rekordbox's database up before a push is unconfirmed until a "
        "push is read"
        if backups is None
        else (
            f"{backups} is where its source says it backs rekordbox's database up "
            f"before a push, unconfirmed until a push is read"
        )
    )
    no_push = "DEADCA7 is installed here and has recorded no push into rekordbox's database: "
    if support is None:
        # Unread is not none: it could not look, never that nothing was pushed.
        return said(
            f"DEADCA7 is installed here ({', '.join(map(str, found))}), and when it last "
            f"pushed into rekordbox's database cannot be said: " + "; ".join(unread)
        )
    if not support:
        return said(
            f"{no_push}{', '.join(map(str, found))} is here, and no push backup folder is. "
            f"{unconfirmed}"
        )
    assert backups is not None  # the support folder is here, so it was named
    presence = _folder_presence(backups)
    try:
        if isinstance(presence, OSError):
            raise presence
        pushed = _newest_entry(backups) if presence else None
    except OSError as exc:
        # Unread is not none: it could not look, never that nothing was pushed.
        return said(
            f"DEADCA7 is installed here, and when it last pushed into rekordbox's "
            f"database cannot be said: its backup folder could not be read ({_said(exc)})"
        )
    if pushed is None:
        held = "holds no entry" if presence else "does not exist"
        return said(f"{no_push}its backup folder {held}. {unconfirmed}")
    when = pushed.strftime("%Y-%m-%d %H:%M UTC")
    run_one = "Run one with: crate backup run"
    try:
        ages = backup_facts.ages(inputs.cfg, now=inputs.probes.now)
    except backup_facts.BackupFactsUnreadable:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"DEADCA7 last pushed into rekordbox's database at {when}; whether this "
                f"product's last backup is newer cannot be said, since the backup record "
                f"could not be read (see backup.age.database)"
            ),
        )
    database = next(entry for entry in ages if entry.portion is backup_facts.Portion.DATABASE)
    if database.state is backup_facts.AgeState.RECORDED_IN_THE_FUTURE:
        # A record backup.age.database calls unusable answers nothing here.
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"DEADCA7 last pushed into rekordbox's database at {when}; whether this "
                f"product's last backup holds it cannot be said, since that backup is "
                f"recorded ahead of now (see backup.age.database)"
            ),
        )
    if database.state is backup_facts.AgeState.NEVER_RECORDED:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"warning: DEADCA7 last pushed into rekordbox's database at {when}, and no "
                f"database backup is recorded here, so nothing this product holds has "
                f"that push in it. {run_one}"
            ),
        )
    completed = database.completed_at
    if completed is not None and pushed > completed:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"warning: DEADCA7 last pushed into rekordbox's database at {when}, after "
                f"this product's last database backup at "
                f"{completed.strftime('%Y-%m-%d %H:%M UTC')}, so that backup does not "
                f"hold the push. {run_one}"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=(
            f"DEADCA7 last pushed into rekordbox's database at {when}, before this "
            f"product's last database backup, which holds it"
        ),
    )


@dataclass(frozen=True, slots=True)
class TrashPolicy:
    """What one rclone remote type does with a deleted object, as a declaration.

    ``option`` is the setting that turns trashing off and ``disabled`` the value
    that means off, since providers disagree on the sense (Drive's ``use_trash``
    false, OneDrive's ``hard_delete`` true). ``option`` None is a provider with
    no escape, a note rather than a failure since nothing can be set (P7).
    ``applies_when`` names the account kind setting and the values on which
    ``option`` is honoured at all; outside them the answer is a note.
    """

    option: str | None
    disabled: str = "false"
    applies_when: tuple[str, frozenset[str]] | None = None


#: What each rclone remote type does on delete, since a prune on a trashing
#: provider reclaims nothing until its retention expires. A type with no row is
#: "not asserted", never fine; only a row reaches OK.
_REMOTE_TRASH_POLICY: Mapping[str, TrashPolicy] = MappingProxyType(
    {
        "drive": TrashPolicy(option="use_trash", disabled="false"),
        "onedrive": TrashPolicy(
            option="hard_delete",
            disabled="true",
            applies_when=("drive_type", frozenset({"business", "documentLibrary"})),
        ),
        # All three keep deleted files and none has a per remote way out
        # (checked against rclone 1.74.3's backend help).
        "dropbox": TrashPolicy(option=None),
        "box": TrashPolicy(option=None),
        "pcloud": TrashPolicy(option=None),
    }
)


#: Remote types where a delete is an unlink, so a prune reclaims space at once.
_NON_TRASHING_REMOTE_TYPES: frozenset[str] = frozenset({"local", "sftp", "ftp"})


def _check_backup_remote(inputs: _Inputs) -> Finding:
    key, title = "backup.remote", "backup remote"
    if inputs.cfg is None:
        return _unchecked(key, title)
    if "backup" not in inputs.membership.modules:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail="the backup module is off in this profile",
        )
    remote = inputs.cfg.backup.remote
    if not remote:
        # INFO, since the full preset turns the module on for everybody and the
        # backup verb refuses on its own missing destination (P7).
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                "the backup module is on and no backup destination is recorded, "
                "so the backup verb has nowhere to write. Run setup and take the "
                "offer, or pass --backup-dest, --backup-archive-root and "
                "--backup-db-dest-root, each an rclone remote:path"
            ),
        )
    rclone = inputs.probes.find_binary("rclone")
    if rclone is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"backup.remote is {remote!r}; rclone is not installed here, so its "
                f"configuration could not be read. The missing binary is reported "
                f"under its own check"
            ),
        )
    remotes = inputs.probes.rclone_remotes(rclone)
    if remotes is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=f"backup.remote is {remote!r}; rclone's configuration could not be read",
        )
    # The remote name is what precedes the colon in rclone's ``remote:path``.
    named = remote.split(":", 1)[0]
    settings = remotes.get(named)
    if settings is None:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            # Not "backup.remote names", since the value may be derived from
            # the destinations and absent from the file.
            detail=(
                f"the backup remote is {remote!r}, from backup.remote or derived "
                f"from the destinations, and rclone has no remote called "
                f"{named!r}; it knows {', '.join(sorted(remotes)) or 'none'}"
            ),
            # Not run setup, which would hand the same name back (R-345).
            remedy=Remedy.FIX_CONFIG_VALUES,
        )
    kind = str(settings.get("type", ""))
    if kind in _NON_TRASHING_REMOTE_TYPES:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                f"{named!r} is a {kind} remote, where a delete is a delete, so a "
                f"prune reclaims its space immediately"
            ),
        )
    policy = _REMOTE_TRASH_POLICY.get(kind)
    if policy is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{named!r} is a {kind or 'typeless'} remote, which this check has "
                f"no row for, so nothing was asserted about whether a pruned "
                f"archive keeps counting against the quota. Providers that trash "
                f"on delete are named one by one here rather than assumed absent"
            ),
        )
    if policy.option is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{named!r} is a {kind} remote. That provider moves a deleted "
                f"object to a recycle bin and offers no per-remote option to stop "
                f"it, so a pruned archive keeps counting against the quota until "
                f"the provider's own retention expires. There is nothing to set; "
                f"emptying it is done at the provider"
            ),
        )
    if policy.applies_when is not None:
        setting, honoured = policy.applies_when
        value = str(settings.get(setting, ""))
        if value not in honoured:
            return Finding(
                key=key,
                title=title,
                status=Status.INFO,
                detail=(
                    f"{named!r} is a {kind} remote whose {setting} is "
                    f"{value or 'unset'}. rclone honours {policy.option} only where "
                    f"{setting} is {' or '.join(sorted(honoured))}, so on this remote "
                    f"it cannot stop a pruned archive going to the recycle bin, and "
                    f"whatever it is set to says nothing about the quota. Emptying it "
                    f"is done at the provider"
                ),
            )
    if str(settings.get(policy.option, "")).lower() == policy.disabled:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                f"{named!r} is a {kind} remote with {policy.option} set to "
                f"{policy.disabled}, so a prune reclaims space"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"{named!r} is a {kind} remote and its {policy.option} option is not "
            f"{policy.disabled}. A pruned archive folder goes to the provider's "
            f"trash and keeps counting against the quota for the retention period, "
            f"which is the whole point of pruning. Set {policy.option} to "
            f"{policy.disabled} on that remote in rclone's own configuration"
        ),
    )
