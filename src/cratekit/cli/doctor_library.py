"""Doctor's checks of the interpreter, the configuration, the library, the taxonomy and rekordbox.
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType

from cratekit.cli import render
from cratekit.cli.doctor_model import Finding, Status, _Inputs, _unchecked, satisfies
from cratekit.core import (
    active_taxonomy,
    config,
    preflight,
    processes,
    taxonomy,
    taxonomy_upgrade,
)
from cratekit.core.cause import (
    CratekitError,
    access_remedy,
)
from cratekit.core.exit_codes import Remedy
from cratekit.write import metadata_cli


def _check_interpreter(inputs: _Inputs) -> Finding:
    running = ".".join(str(part) for part in inputs.probes.python_version)
    declared = inputs.probes.requires_python
    key, title = "interpreter.version", "supported Python"
    if not declared:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"running Python {running}; the supported range could not be read "
                f"from this installation's packaging metadata, so nothing was "
                f"asserted about it"
            ),
        )
    verdict = satisfies(inputs.probes.python_version, declared)
    if verdict is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"running Python {running}; the declared range {declared!r} is not "
                f"in a shape this check understands, so nothing was asserted"
            ),
        )
    if verdict:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=f"Python {running} is inside the supported range {declared}",
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"Python {running} is outside the supported range {declared}. The "
            f"vendored downloader has never run on it, and the failure that "
            f"follows names a dependency rather than the interpreter"
        ),
        # Reused rather than adding a near synonym: the interpreter is part of
        # the platform, and the token means "this environment cannot run it".
        remedy=Remedy.UNSUPPORTED_PLATFORM,
    )


def _check_config(inputs: _Inputs) -> Finding:
    key, title = "config.present", "configuration"
    if inputs.cfg is not None:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=f"loaded from {config.config_path()}",
        )
    error = inputs.config_error
    if error is None:  # pragma: no cover - run() sets one whenever cfg is None
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail="no configuration was supplied and none could be loaded",
            remedy=Remedy.RUN_SETUP,
        )
    # ``ConfigError.remedy`` is declared on every subclass, so it is read
    # directly, since the failures do not share one remedy. An OS refusal
    # overrules it, because an unreadable config is intact and needs access, not
    # a rewrite.
    note = render.access_note(error)
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=str(error) + (f". {note}" if note else ""),
        remedy=access_remedy(error, otherwise=Remedy(str(error.remedy))),
    )


#: One sentence per mount outcome, since "not mounted" and "mounted somewhere
#: else" have different fixes.
_MOUNT_DETAIL: Mapping[preflight.MountState, str] = MappingProxyType(
    {
        preflight.MountState.OK: "the recorded volume is mounted at the configured root",
        preflight.MountState.NOT_MOUNTED: (
            "the recorded volume is not mounted anywhere and the configured root "
            "does not exist. Attach it"
        ),
        preflight.MountState.MOUNTED_ELSEWHERE: (
            "the recorded volume IS attached, at a different mount point than the "
            "configured root. Nothing needs plugging in; the configured root is "
            "pointing at the wrong place"
        ),
        preflight.MountState.FOREIGN_VOLUME: (
            "a DIFFERENT volume occupies the configured root. A restored clone "
            "looks healthy from the outside and is the case this check exists for"
        ),
        preflight.MountState.LIBRARY_PATH_MISSING: (
            "the recorded volume is mounted and the configured root is not a "
            "directory on it, so the library was moved within the volume"
        ),
        preflight.MountState.IDENTITY_UNAVAILABLE: (
            "the filesystem at the configured root reports no volume identity, so "
            "a clone mounted in its place could not be told apart from it"
        ),
        preflight.MountState.IDENTITY_NOT_RECORDED: (
            "no volume identity was recorded for this library, so nothing can be "
            "asserted before a destructive write"
        ),
    }
)


def _check_library_mounted(inputs: _Inputs) -> Finding:
    key, title = "library.mounted", "library volume"
    status = inputs.mount()
    if status is None:
        return _unchecked(key, title)
    described = _MOUNT_DETAIL[status.state]
    where = f" (configured root {status.configured_root})"
    if status.state is preflight.MountState.MOUNTED_ELSEWHERE:
        where = f" (configured root {status.configured_root}, found at {status.found_at})"
    if status.state is preflight.MountState.OK:
        return Finding(key=key, title=title, status=Status.OK, detail=described + where)
    if status.state in (
        preflight.MountState.IDENTITY_UNAVAILABLE,
        preflight.MountState.IDENTITY_NOT_RECORDED,
    ):
        # The identity check answers these, so one problem is reported once.
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=f"the identity question is answered by its own check{where}",
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=described + where,
        remedy=Remedy.MOUNT_LIBRARY_VOLUME,
    )


#: What the identity question answers for each mount outcome, as a total
#: mapping with no fall-through, so only the two states meaning "observed equals
#: recorded" can read green.
_IDENTITY_VERDICT: Mapping[preflight.MountState, tuple[Status, Remedy | None]] = (
    MappingProxyType(
        {
            preflight.MountState.OK: (Status.OK, None),
            # The volume matched; the missing directory is the mount check's.
            preflight.MountState.LIBRARY_PATH_MISSING: (Status.OK, None),
            preflight.MountState.IDENTITY_NOT_RECORDED: (Status.FAIL, Remedy.RUN_SETUP),
            preflight.MountState.IDENTITY_UNAVAILABLE: (
                Status.FAIL,
                Remedy.UNSUPPORTED_PLATFORM,
            ),
            preflight.MountState.FOREIGN_VOLUME: (Status.FAIL, Remedy.MOUNT_LIBRARY_VOLUME),
            # The mount check's question; the recorded identity is intact.
            preflight.MountState.NOT_MOUNTED: (Status.INFO, None),
            preflight.MountState.MOUNTED_ELSEWHERE: (Status.INFO, None),
        }
    )
)


def _check_library_identity(inputs: _Inputs) -> Finding:
    key, title = "library.identity", "library volume identity"
    status = inputs.mount()
    if status is None:
        return _unchecked(key, title)
    verdict, remedy = _IDENTITY_VERDICT[status.state]
    if verdict is Status.OK:
        detail = f"the observed identity matches the recorded {status.recorded_identity}"
    elif status.state is preflight.MountState.FOREIGN_VOLUME:
        detail = (
            f"recorded identity {status.recorded_identity}, observed "
            f"{status.observed_identity}: {_MOUNT_DETAIL[status.state]}"
        )
    elif verdict is Status.INFO:
        # The observed identity is named anyway, since nothing else prints it
        # and ``--volume-id`` needs it to replace a wrong recorded one.
        detail = (
            f"nothing at the configured root to compare: {_MOUNT_DETAIL[status.state]}. "
            f"The recorded identity {status.recorded_identity} is intact; the "
            f"filesystem at {status.mount_point} reports "
            f"{status.observed_identity or 'no identity'}"
        )
    else:
        detail = _MOUNT_DETAIL[status.state]
    return Finding(key=key, title=title, status=verdict, detail=detail, remedy=remedy)


def _check_db_containment(inputs: _Inputs) -> Finding:
    """An accepted database outside the library root is reported on every run.

    So a person who accepted it long ago is still told their snapshots are
    copies across two filesystems rather than one atomic commit (U27).
    """
    key, title = "library.db_containment", "database and library on one filesystem"
    if inputs.cfg is None:
        return _unchecked(key, title)
    cfg = inputs.cfg
    if cfg.db_is_inside_library_root():
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                "library.db_path sits under library.root, so a snapshot commits "
                "atomically with a rename"
            ),
        )
    accepted = cfg.library.db_outside_root_acknowledged_on
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=(
            f"library.db_path ({cfg.library.db_path}) is outside library.root "
            f"({cfg.library.root}), accepted on {accepted}. A snapshot of the "
            f"database and its coupled state therefore spans two filesystems and "
            f"is a copy rather than one atomic commit, so a crash mid-capture can "
            f"leave the two halves describing different moments"
        ),
    )


def _check_trash(inputs: _Inputs) -> Finding:
    """Whether the library volume has a Trash this account can move a file into.

    A confirmed deletion goes to the Trash, never an unlink (R35), so this says
    beforehand what would otherwise refuse mid deletion. It does not defer to
    the mount checks, since a read only volume passes both and still has no
    usable Trash. Asked with ``create=False`` so it cannot pass by having run.
    """
    key, title = "library.trash", "system Trash on the library volume"
    if inputs.cfg is None:
        return _unchecked(key, title)
    root = inputs.cfg.library.root
    try:
        status = inputs.probes.trash_probe(root)
    except OSError as exc:
        # Gated on ``required``: unanswered is not a pass, but nor is it red on a
        # profile where nothing trashes a file.
        needed = inputs.required(key)
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL if needed else Status.INFO,
            detail=(
                f"whether {root} has a usable Trash could not be established "
                f"({exc}), so whether a confirmed deletion would land in the "
                f"Trash or refuse is unknown"
            ),
            remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT) if needed else None,
            error=exc if needed else None,
        )
    if status.usable:
        where = status.layout.files if status.layout is not None else root
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=f"{where} exists on the same filesystem as {root} and accepts a move",
        )
    if status.absent:
        # Not a failure: the deletion pass creates the Trash on first use, so a
        # fresh volume works, and red here would predict a refusal that never
        # comes.
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                f"{root} has no Trash directory yet, which is the state of a "
                f"volume nobody has deleted from; the deletion pass creates it on "
                f"first use exactly as the desktop does"
            ),
        )
    if not inputs.required(key):
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{status.problem}, and no verb this profile switches on moves a "
                f"file to the Trash, so nothing depends on it today"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"{status.problem}. A confirmed deletion moves the file to the "
            f"volume's own Trash and never unlinks it, so this profile switches "
            f"on a verb that would refuse partway through a deletion rather than "
            f"before one"
        ),
        # Not ``RUN_DOCTOR``, which would loop back here. Missing and unwritable
        # are a path to grant; another filesystem is named in the sentence.
        remedy=Remedy.GRANT_PATH_ACCESS,
    )


def _library_state_unreadable(inputs: _Inputs, what: str) -> str | None:
    """Why library-scoped state may not be read here, or None when it may.

    A missing file and a missing volume look the same, so ``core/preflight``'s
    rule tells them apart. Callers report it as INFO, since the volume is one
    problem reported once by its own checks, and a run setup remedy against an
    absent volume would be wrong.
    """
    status = inputs.mount()
    if status is None or preflight.library_state_is_readable(status):
        return None
    return (
        f"not asserted: {what} lives on the library volume, and this run could "
        f"not establish that the volume is there ({status.state.value}), so "
        f"nothing at the configured root was read. The volume is reported by its "
        f"own checks"
    )


def _volume_clause(inputs: _Inputs) -> str:
    """What an OK detail may claim about the disk it just read from.

    Derived from ``_IDENTITY_VERDICT``, so it never claims the recorded volume
    when the identity check could not compare one.
    """
    status = inputs.mount()
    if status is not None and _IDENTITY_VERDICT[status.state][0] is Status.OK:
        return "on the recorded library volume"
    return (
        "at the configured root, on a volume whose identity could not be "
        "compared here, so which disk it is was not established"
    )


def _check_taxonomy_schema(inputs: _Inputs) -> Finding:
    """The active copy's schema version against the shipped one, and each entry it lacks (U132).

    INFO, never FAIL, since a missing bucket may be a person's decision; a copy
    that cannot be read is ``taxonomy.active``'s failure. The planner reads the
    shipped text, so doctor holds no parsed shipped taxonomy.
    """
    key, title = "taxonomy.schema", "active taxonomy against the shipped schema"
    if inputs.cfg is None:
        return _unchecked(key, title)
    unreadable = _library_state_unreadable(inputs, "the active template")
    if unreadable is not None:
        return Finding(key=key, title=title, status=Status.INFO, detail=unreadable)
    try:
        _, found = taxonomy_upgrade.planned(inputs.cfg)
    except taxonomy_upgrade.NoCopy:
        # No copy is not a copy behind: every verb routes by the shipped template.
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                f"this library holds no active taxonomy copy, so every verb routes by the "
                f"shipped {inputs.cfg.taxonomy.template!r} template, which is current"
            ),
        )
    except taxonomy_upgrade.ShippedUnreadable as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"not compared: {exc.cause.message}. The shipped template is the one "
                f"taxonomy.template names in the configuration"
            ),
        )
    except CratekitError as exc:
        if exc.cause.reason == "internal-error":
            # Packaged data failed to compare, a defect rather than the person's copy.
            return Finding(
                key=key,
                title=title,
                status=Status.FAIL,
                detail=exc.cause.message,
                remedy=Remedy.REPORT_DEFECT,
            )
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"not compared: {exc.cause.message}. taxonomy.active reports the copy "
                f"itself"
            ),
        )
    if not found.behind:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail=(
                f"the active copy states schema_version {found.from_version} and the "
                f"shipped {found.template!r} template states {found.shipped_version}, and "
                f"the copy declares every class, bucket and vocabulary table it ships"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.INFO,
        detail=f"{taxonomy_upgrade.gap(found)}. {taxonomy_upgrade.remedy(found)}",
    )


def _origin_verdict(cfg: config.Config, active_text: str, named: str) -> tuple[Status, str]:
    """Whether the active copy fell behind the shipped template, or was edited (R-689).

    Compares three digests: setup's record, the copy now, and the shipped text
    now. An unedited copy behind a changed template is INFO; an edited copy is
    the person's; with no record the two cannot be told apart and the detail
    says so. A record naming another template is also INFO. It never writes,
    and reads the shipped template only as a fingerprint.
    """
    origin_path = config.state_path("taxonomy_origin", cfg)
    record: taxonomy.Origin | None
    try:
        record_text = origin_path.read_text(encoding="utf-8")
    except (FileNotFoundError, NotADirectoryError):
        record = None
    except (OSError, UnicodeDecodeError) as exc:
        return Status.INFO, (
            f"the record of which shipped text the copy was made from, at "
            f"{origin_path}, could not be read ({exc}), so a copy that fell "
            f"behind the shipped template cannot be told from one a person edited"
        )
    else:
        try:
            record = taxonomy.parse_origin_record(record_text)
        except ValueError as exc:
            return Status.INFO, (
                f"the record of which shipped text the copy was made from, at "
                f"{origin_path}, is not usable ({exc}), so a copy that fell "
                f"behind the shipped template cannot be told from one a person "
                f"edited"
            )
    if record is not None and record.template != named:
        # The configured name and the copy disagree, and every verb reads the copy.
        return Status.INFO, (
            f"the copy was made from the shipped {record.template!r} and "
            f"taxonomy.template now names {named!r}; every verb reads the copy, "
            f"so this library declares the tree of {record.template!r}, and a "
            f"re-run of setup leaves an existing copy alone"
        )
    active = taxonomy.template_fingerprint(active_text)
    # ``named`` ships, so failing to read it means a damaged install.
    try:
        current = taxonomy.shipped_template_fingerprint(named)
    except (OSError, UnicodeDecodeError) as exc:
        return Status.INFO, (
            f"the packaged text of {named!r} could not be read ({exc}), so the "
            f"copy was compared with nothing and whether it fell behind the "
            f"shipped template was not established. This is a damaged or partial "
            f"install"
        )
    if record is None:
        if active.digest == current.digest:
            return Status.OK, (
                f"nothing records which shipped text the copy was made from, "
                f"and it matches the shipped {named!r} as it ships now"
            )
        return Status.OK, (
            f"nothing records which shipped text the copy was made from, and it "
            f"differs from the shipped {named!r} as it ships now, so whether it "
            f"was edited or fell behind the shipped template cannot be told. "
            f"Setup records the origin only for a copy it makes"
        )
    if active.digest != record.digest:
        return Status.OK, f"edited since setup copied the shipped {record.template!r}"
    if current.digest == record.digest:
        return Status.OK, (
            f"unedited since setup copied the shipped {record.template!r}, which "
            f"has not changed since"
        )
    gained = sorted(current.sections - active.sections)
    dropped = sorted(active.sections - current.sections)
    changes = []
    if gained:
        changes.append(
            f"it now declares {', '.join(f'[{name}]' for name in gained)}, which "
            f"the copy does not"
        )
    if dropped:
        changes.append(
            f"it no longer declares {', '.join(f'[{name}]' for name in dropped)}, "
            f"which the copy still does"
        )
    change = "; ".join(changes) or "the difference is inside sections both declare"
    return Status.INFO, (
        f"the copy is the one setup made from the shipped {record.template!r}, "
        f"unedited, and that template has changed since: {change}. Every verb "
        f"reads the copy, so nothing the shipped template changed applies to this "
        f"library until it is copied in, by hand or, for a class, a bucket or a "
        f"vocabulary table, by "
        f"{taxonomy_upgrade.VERB}; doctor does not rewrite the copy"
    )


def _check_rekordbox_closed(inputs: _Inputs) -> Finding:
    key, title = "rekordbox.closed", "rekordbox not running"
    try:
        running = processes.rekordbox_processes_running(lister=inputs.probes.process_lister)
    except processes.AbsenceUnconfirmed as exc:
        # A note, never a pass (U211): absence is unknown, and it clears once the
        # process exits, while every write refuses on its own until then.
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{exc.cause.message}. Every database write refuses until the scan "
                f"reads clean, which it does once the process finishes exiting; a "
                f"zombie is skipped and never reported"
            ),
        )
    if not running:
        return Finding(
            key=key,
            title=title,
            status=Status.OK,
            detail="neither the application nor its background agent is running",
        )
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"{', '.join(running)} running. The agent is the one that surprises "
            f"people: it holds the database and mutates it through Cloud Library "
            f"Sync with the window closed"
        ),
        remedy=Remedy.QUIT_REKORDBOX,
    )


def _check_rekordbox_pins(inputs: _Inputs) -> Finding:
    key, title = "rekordbox.pins", "rekordbox version pins"
    if inputs.cfg is None:
        return _unchecked(key, title)
    cfg = inputs.cfg
    binding = inputs.probes.binding_pin_problem(cfg)
    if binding is not None:
        return Finding(
            key=key, title=title, status=Status.FAIL, detail=binding,
            remedy=Remedy.REVALIDATE_PINS,
        )
    pinned = cfg.rekordbox.pinned_app_version
    installed = inputs.probes.installed_app_version(cfg)
    if not pinned:
        # An unset pin is never adopted from the installed version, since such a
        # pin would refuse nothing (S2).
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"no rekordbox application version is pinned, so every database "
                f"write refuses. The installed version is "
                f"{installed or 'not locatable from here'}, and recording a pin is "
                f"a deliberate act rather than a value this reads off the machine"
            ),
            remedy=Remedy.RECORD_REKORDBOX_PIN,
        )
    if installed is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"pinned at {pinned}; the installed application could not be "
                f"located, so the schema pin is the only one still asserting"
            ),
        )
    if installed != pinned:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"installed rekordbox {installed} does not match the recorded pin "
                f"{pinned}, so database writes are frozen by design rather than "
                f"broken"
            ),
            remedy=Remedy.REVALIDATE_PINS,
        )
    validated = cfg.rekordbox.validated_on
    if not validated:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"pinned at {pinned} and matching, with no recorded date on which "
                f"the pin was confirmed against a real write. Without that date a "
                f"pin is a number somebody typed"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.OK,
        detail=f"pinned at {pinned}, matching, confirmed against a write on {validated}",
    )


def _copy_withheld(inputs: _Inputs, key: str, title: str, question: str) -> Finding | None:
    """Why no copy of the database may be taken for ``question`` now, or None when one may.

    Rekordbox is asked about first, since a copy taken under it is torn, then the
    volume, so a stale mount point is not surveyed. An unconfirmed absence is a
    note (U211); a running rekordbox FAIL with the act that unblocks it.
    """
    try:
        running = processes.rekordbox_processes_running(lister=inputs.probes.process_lister)
    except processes.AbsenceUnconfirmed as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{question} was not established: {exc.cause.message}, so no copy of "
                f"the database was taken. The answer is unknown rather than good"
            ),
        )
    if running:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"{question} could not be established: {', '.join(running)} running, "
                f"and a copy of the database taken under a live application is "
                f"incomplete, so none was taken. The answer is unknown rather than good"
            ),
            remedy=Remedy.QUIT_REKORDBOX,
        )
    unreadable = _library_state_unreadable(inputs, "the database")
    if unreadable is not None:
        return Finding(key=key, title=title, status=Status.INFO, detail=unreadable)
    return None


def _copy_unopened(key: str, title: str, question: str, exc: CratekitError) -> Finding:
    """FAIL with the open's own cause: a copy of the database would not open."""
    cause = exc.cause
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=(
            f"{question} could not be established: a copy of the database could not "
            f"be opened, {cause.message}. The answer is unknown rather than good, and "
            f"the live file was not touched"
        ),
        remedy=cause.remediation.remedy,
        cause=cause,
    )


def _check_playlist_numbers(inputs: _Inputs) -> Finding:
    """How many of the product's playlists hold live rows not numbered 1 to N (U958).

    rekordbox's Remove from Playlist takes out the row numbered as the shown
    position, so such a playlist loses the wrong track to a removal by hand.
    Read off a disposable copy once rekordbox is known closed, the scope the
    repair's own: ``crate repair numbers`` plans the same playlists. INFO with
    the count and the repair when any, OK when none.
    """
    key, title = "library.playlist_numbers", "the product's playlists are numbered 1 to N"
    if inputs.cfg is None:
        return _unchecked(key, title)
    question = "whether the product's playlists are numbered 1 to N"
    withheld = _copy_withheld(inputs, key, title, question)
    if withheld is not None:
        return withheld
    try:
        declared = active_taxonomy.load(inputs.cfg)
    except CratekitError as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{question} was not established: the taxonomy that names the product's "
                f"nodes could not be read, {exc.cause.message}. The answer is unknown "
                f"rather than good"
            ),
        )
    try:
        planned = inputs.probes.numbers_survey(inputs.cfg, declared)
    except CratekitError as exc:
        return _copy_unopened(key, title, question, exc)
    if planned is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"no database file at {inputs.cfg.library.db_path}, so no playlist was "
                f"read and nothing was asserted about their numbers"
            ),
        )
    held = (
        f"; {len(planned.held)} more hold a row whose removal marker or place cannot "
        f"be read, so their order cannot be said"
        if planned.held
        else ""
    )
    if planned.items:
        shown = ", ".join(repr(one.path) for one in planned.items[:3])
        more = f" and {len(planned.items) - 3} more" if len(planned.items) > 3 else ""
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{len(planned.items)} of {planned.scanned} playlists under this product's "
                f"nodes hold live rows not numbered 1 to N ({shown}{more}), so a removal "
                f"by hand in rekordbox there may take out the wrong track; crate repair "
                f"numbers numbers them 1 to N{held}"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.INFO if planned.held else Status.OK,
        detail=(
            f"all {planned.scanned} playlists under this product's nodes that could be "
            f"read number their live rows 1 to N, read off a disposable copy of the "
            f"database{held}"
        ),
    )


def _check_paths_resolved(inputs: _Inputs) -> Finding:
    """Whether the collection's recorded paths can be read from this machine.

    Reads the ratio the My Tags plan refuses on, off a disposable copy, so a
    person learns before the plan (R-372). Rekordbox is asked about first, since
    a copy taken under it is torn, then the volume, so a stale mount point is not
    surveyed. Not gated on ``required``: core verbs on every profile resolve
    paths.

    No database file is INFO; a copy that will not open is FAIL with the open's
    own cause; a majority of rows under no rule is FAIL under the plan's own
    slug, so the two cannot disagree; a minority is INFO with the count.
    """
    key, title = "library.paths_resolved", "recorded paths resolve on this machine"
    if inputs.cfg is None:
        return _unchecked(key, title)
    cfg = inputs.cfg
    question = "whether the collection's rows resolve"
    withheld = _copy_withheld(inputs, key, title, question)
    if withheld is not None:
        return withheld
    try:
        totals = inputs.probes.path_survey(cfg)
    except CratekitError as exc:
        return _copy_unopened(key, title, question, exc)
    if totals is None:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"no database file at {cfg.library.db_path}, so no row was read and "
                f"nothing was asserted about how the collection resolves"
            ),
        )
    rules = len(cfg.library.location_prefix_map)
    if totals.majority_unmapped:
        cause = metadata_cli.majority_unmapped_cause(cfg, totals)
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"{cause.message}. The My Tags plan reads ok over such a library "
                f"with every one of those rows skipped, and an apply writes nothing"
            ),
            remedy=cause.remediation.remedy,
            cause=cause,
        )
    if totals.unmapped:
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"{totals.unmapped} of {totals.active} active rows record a path "
                f"under no library.location_prefix_map rule, a minority, with "
                f"{rules} rule{'s' if rules != 1 else ''} recorded; those rows are "
                f"skipped by every pass that resolves paths, and {totals.unresolved} "
                f"rows in all resolve to no file here"
            ),
        )
    return Finding(
        key=key,
        title=title,
        status=Status.OK,
        detail=(
            f"every one of {totals.active} active rows records a path under the "
            f"library root or a recorded rule ({rules} rule"
            f"{'s' if rules != 1 else ''}), read off a disposable copy of the "
            f"database; {totals.unresolved} resolve to no file here"
        ),
    )
