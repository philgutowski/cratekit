"""Doctor's checks of the interpreter, the configuration, the library, the taxonomy and rekordbox.
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType

from cratekit.cli import render
from cratekit.cli.doctor_model import Finding, Status, _Inputs, _unchecked, satisfies
from cratekit.core import (
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
        # UNSUPPORTED_PLATFORM is reused rather than joined by a near synonym.
        # The exit-code vocabulary's own docstring records three re-authentication
        # tokens it will not collapse because each is already a persisted slug,
        # and the lesson runs the other way too: a new token whose meaning is
        # inside an existing one is a second name for one idea. The running
        # interpreter is part of the platform this install is on, and the token
        # already means "this environment cannot run the operation".
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
    # ``ConfigError.remedy`` is a declared class attribute on every member of the
    # hierarchy, so it is read directly. A ``getattr`` with a default here would
    # hand back a permissive answer for a field whose whole purpose is that the
    # five failures do NOT share one remediation.
    #
    # AND THEN THE CLASSIFICATION OVERRULES IT WHEN THE OPERATING SYSTEM IS WHAT
    # REFUSED. A config file with mode 0o000 is byte for byte intact, and this
    # check reported "repair or recreate it" over it, which is a report telling
    # its reader to rewrite a file that is perfectly good. The declared remedy
    # stands for every other way a config can be unusable.
    note = render.access_note(error)
    return Finding(
        key=key,
        title=title,
        status=Status.FAIL,
        detail=str(error) + (f". {note}" if note else ""),
        remedy=access_remedy(error, otherwise=Remedy(str(error.remedy))),
    )


#: One sentence per mount outcome, and the whole reason there are six of them.
#: "Not mounted" and "mounted somewhere else" have different fixes, and a report
#: that says only "the volume is wrong" sends the user to unplug a drive that was
#: never the problem.
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
        # Both are the IDENTITY question and are answered by the next check.
        # Repeating them here as a failure would report one problem twice and
        # attach the wrong fix to one of the copies.
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


#: What the IDENTITY question answers for each mount outcome, as a TOTAL mapping
#: over the enum rather than as a chain of branches with a fall-through at the end.
#:
#: The fall-through is what makes the branch shape wrong here, and it was wrong
#: for two states before this table existed. ``resolve_mount_state`` populates
#: ``observed_identity`` for NOT_MOUNTED and MOUNTED_ELSEWHERE alike, because it
#: observed SOMETHING at the configured path in both cases, so a final "and
#: otherwise the identity matched" reported a green identity beside a red mount
#: for a volume that is somewhere else entirely, and for one that is not attached
#: at all. Only two states mean the observed identity equalled the recorded one,
#: and they are named here rather than inferred.
_IDENTITY_VERDICT: Mapping[preflight.MountState, tuple[Status, Remedy | None]] = (
    MappingProxyType(
        {
            preflight.MountState.OK: (Status.OK, None),
            # The volume matched; what is missing is a directory ON it, which is
            # the mount check's answer rather than this one's.
            preflight.MountState.LIBRARY_PATH_MISSING: (Status.OK, None),
            preflight.MountState.IDENTITY_NOT_RECORDED: (Status.FAIL, Remedy.RUN_SETUP),
            preflight.MountState.IDENTITY_UNAVAILABLE: (
                Status.FAIL,
                Remedy.UNSUPPORTED_PLATFORM,
            ),
            preflight.MountState.FOREIGN_VOLUME: (Status.FAIL, Remedy.MOUNT_LIBRARY_VOLUME),
            # Both of these are the MOUNT question. The recorded identity is
            # intact and reporting it as a second failure would attach a fix to a
            # problem that is not this one.
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
        # The OBSERVED identity is named even here, where it is not the answer.
        # ``--volume-id`` is the only way to replace a recorded identity, by
        # design, and a user whose configuration carries the wrong one has no
        # other way to learn what the right one is: nothing else in the product
        # prints a volume's identity. A refusal that cannot be acted on is a
        # refusal people work around.
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
    """An accepted database outside the library root is reported on EVERY run.

    ``tests/_pending.py`` held this against U27 rather than leaving it in a
    docstring, and the reason is in ``core/config``: refusing at load makes the
    consequence visible at setup, when the user can still move the database, and
    does nothing at all about the install where somebody accepted it eighteen
    months ago and has since forgotten that their snapshots are copies across two
    filesystems rather than one atomic commit. This is the run that keeps saying
    so.
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

    R35 sends a confirmed deletion to the system Trash and never to an unlink, so
    a volume with no usable Trash is a volume on which the deletion pass refuses.
    Without this check a person meets that refusal in the middle of a deletion,
    after the review, after the confirm gate, with a plan already digested. This
    is the run that says so beforehand.

    IT DOES NOT DEFER TO THE MOUNT CHECKS, unlike the two library-scoped state
    readers below, and the difference is real rather than an oversight. Those two
    read a file this product WROTE under the library root, so an absent volume
    means there is nothing to read and the volume is one problem reported once.
    This asks whether a specific directory on that volume will accept a move, and
    the two questions come apart in the direction that matters: a mounted volume
    with the recorded identity and a read-only mount answers both mount checks
    green and has no usable Trash at all. A foreign volume failing both is not one
    answer twice, it is two preconditions of one destructive act.

    ASKED WITH ``create=False``, through the seam that binds it, so the check
    cannot pass by having run.
    """
    key, title = "library.trash", "system Trash on the library volume"
    if inputs.cfg is None:
        return _unchecked(key, title)
    root = inputs.cfg.library.root
    try:
        status = inputs.probes.trash_probe(root)
    except OSError as exc:
        # GATED ON ``required`` LIKE EVERY NEIGHBOURING CHECK. An unanswerable
        # question is still not a pass, but on a profile where nothing trashes a
        # file it is not a red either, and a report that paints red for a
        # capability nothing uses is how people learn to ignore red.
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
        # NOT A FAILURE, and getting this wrong made the check worse than absent.
        # ``trash.probe`` creates the per-volume Trash on first use because the
        # desktop does, and the deletion pass takes that default. Doctor asks with
        # ``create=False`` so its answer cannot be produced by its own asking,
        # which means a volume nobody has trashed anything on answers "not a
        # directory" here and works perfectly when a deletion actually runs.
        # Driven: probe(create=False) says unusable and probe(create=True) says
        # usable on the same fresh volume. Reporting that as red tells a person
        # deletion will refuse when it will not, which is the one thing a
        # precondition must never do.
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
        # NOT ``RUN_DOCTOR``, which is what ``trash.assert_usable`` refuses with:
        # that token sends a person here, and here answering with it again is a
        # loop. The three shapes this probe reports are a directory that is not
        # there, one this account cannot write, and one on another filesystem,
        # and the first two are a path to grant access to. The third is named in
        # the sentence, because no token in the vocabulary means "your Trash is
        # on the wrong disk" and inventing one for a case a person meets once
        # would be a token nobody ever reads.
        remedy=Remedy.GRANT_PATH_ACCESS,
    )


def _library_state_unreadable(inputs: _Inputs, what: str) -> str | None:
    """Why library-scoped state may not be read here, or None when it may.

    Both callers below report on a file that sits under the library root by
    construction, and for both of them "the file is not there" and "the disk the
    file lives on is not there" produce the same bytes: none. The rule for
    telling those apart is ``core/preflight``'s, because that is the module that
    owns what a mount outcome means.

    The wizard asks a NEIGHBOURING question before it writes one of these files,
    and the two are deliberately separate functions over separate tables: a
    matching identity with an absent root is nothing to read here and exactly the
    right moment to write there.

    The caller reports it as INFO, for the reason the mount check gives when it
    defers to the identity check: the volume is one problem and it is reported
    once, by the checks that own it. Reporting a missing template here would also
    attach the wrong remedy, since running setup against an absent volume is the
    write this unit had to be stopped from making.
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
    """What an OK detail may CLAIM about the disk it just read from.

    Derived from ``_IDENTITY_VERDICT``, the same total mapping the identity check
    itself answers with, so the two can never disagree about whether a comparison
    happened. Only the two outcomes that mean "observed equals recorded" earn the
    strong sentence.

    It exists because the OK details asserted the strong one unconditionally. A
    machine with no identity adapter reaches these checks through the leg of the
    reachability rule whose entire meaning is that the identity could not be
    ASKED, and it then read "on the recorded library volume" on the same report
    as ``library.identity`` failing with "the filesystem at the configured root
    reports no volume identity". That is a positive claim about a disk nobody
    looked at, which is the class of defect this whole pass exists to remove, so
    it may not be reintroduced by the pass itself.
    """
    status = inputs.mount()
    if status is not None and _IDENTITY_VERDICT[status.state][0] is Status.OK:
        return "on the recorded library volume"
    return (
        "at the configured root, on a volume whose identity could not be "
        "compared here, so which disk it is was not established"
    )


def _check_taxonomy(inputs: _Inputs) -> Finding:
    key, title = "taxonomy.active", "active taxonomy template"
    if inputs.cfg is None:
        return _unchecked(key, title)
    unreadable = _library_state_unreadable(inputs, "the active template")
    if unreadable is not None:
        return Finding(key=key, title=title, status=Status.INFO, detail=unreadable)
    shipped, unlistable = taxonomy.shipped_templates()
    named = inputs.cfg.taxonomy.template
    if unlistable is not None:
        # "NOT PRESENT" AND "COULD NOT LOOK" ARE DIFFERENT ANSWERS, and the empty
        # tuple was serving as both. The walk swallows an unreadable packaged
        # directory so that building the command tree cannot die on a partial
        # install, which is right; what was wrong is reading the resulting
        # emptiness as a fact about the shipped set. A user with a damaged
        # install was told their configuration named a template nothing ships and
        # sent to re-run setup, which cannot repair packaged data.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"{unlistable}. Whether a template named {named!r} ships was "
                f"therefore not established, and neither was the active copy "
                f"beside the database. This is a damaged or partial install "
                f"rather than a configuration error, so re-running setup would "
                f"not repair it"
            ),
            remedy=Remedy.REPORT_DEFECT,
        )
    if named not in shipped:
        # ASSERTED rather than assumed, and it was assumed. The OK branch below
        # claimed the configured template "is active" while comparing nothing to
        # that name, so a configuration naming a template that does not ship read
        # green: nothing rejected the name, and the file beside the database is
        # whatever was copied there once, under whatever name.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"taxonomy.template names {named!r} and no template ships under "
                f"that name; shipped: {', '.join(shipped)}. A re-run of setup "
                f"replaces a recorded name the shipped set does not contain"
            ),
            remedy=Remedy.RUN_SETUP,
        )
    path = config.state_path("taxonomy_active", inputs.cfg)
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, NotADirectoryError):
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"no active taxonomy template at {path}. S6 makes the library "
                f"self-describing by copying the chosen template beside the "
                f"database, and routing has no declared tree without it"
            ),
            remedy=Remedy.RUN_SETUP,
        )
    except (OSError, UnicodeDecodeError) as exc:
        # UnicodeDecodeError is a ValueError, not an OSError, so a template that
        # is present and is not text would otherwise escape this check as an
        # internal defect rather than as the unusable template it is.
        #
        # AND IT IS A SEPARATE ANSWER FROM "IT IS NOT THERE". One handler over
        # both said "no active taxonomy template at X" for a file that is at X
        # and cannot be read by this account, and then attached run-setup, which
        # takes the branch below that leaves an existing file alone. The user
        # re-runs setup forever.
        #
        # AND IT DOES NOT CLAIM THE FILE EXISTS. It said "exists and could not be
        # read", and the exception that lands here does not establish existence:
        # a permission error raised by an untraversable PARENT arrives on this
        # branch, and nothing under such a parent has been observed at all.
        # Asserting a file is at a path nobody could look at is the same defect,
        # one line further on, as the one this handler was split out to fix.
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"the active taxonomy template at {path} could not be read "
                f"({exc}), so whether the library declares a usable tree was not "
                f"established. Whether the file is even there is unknown too: a "
                f"directory on the way to it that this account cannot open fails "
                f"the same way. Setup leaves an existing copy alone, so this is a "
                f"permission or a corruption to repair rather than an answer to "
                f"give again"
            ),
            # The sentence already names a permission as one of the two shapes,
            # and the remedy has to name the same two. A corruption is a defect
            # to report and a permission is one to grant, so the token follows
            # the classification rather than assuming the worse of the user.
            remedy=access_remedy(exc, otherwise=Remedy.REPORT_DEFECT),
        )
    try:
        declared = taxonomy.load_taxonomy(text)
    except taxonomy.TaxonomyError as exc:
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=f"the active taxonomy template at {path} is not usable: {exc}",
            remedy=Remedy.RUN_SETUP,
        )
    status, origin = _origin_verdict(inputs.cfg, text, named)
    return Finding(
        key=key,
        title=title,
        status=status,
        detail=(
            f"an active template at {path}, {_volume_clause(inputs)}, parses and "
            f"declares {len(declared.buckets)} buckets; taxonomy.template names "
            f"the shipped {named!r}; {origin}"
        ),
    )


def _check_taxonomy_schema(inputs: _Inputs) -> Finding:
    """The active copy's schema version against the shipped one, and each entry it lacks (U132).

    THE CHECK THE LIVE LIBRARY NEEDED. Its copy stated ``schema_version = 2``
    with no genre Favorites class long after one shipped, and every Favorites
    step refused or skipped over it while doctor read the copy as parsing and
    said nothing more. This names both versions, every shipped class and bucket
    the copy lacks, what ``crate taxonomy upgrade`` would add, and the hand edit
    each entry it holds needs.

    INFO, NEVER FAIL. A copy without a bucket the shipped template has may be a
    person's decision, and a red line over it trains people to ignore red. A
    copy that does not load or cannot be read is ``taxonomy.active``'s failure
    and is not reported a second time here.

    THE SHIPPED TEXT STAYS OUT OF THIS MODULE. The planner reads it and answers
    in names and sentences, so doctor still holds no parsed shipped taxonomy.
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
        # No copy is not a copy behind: every verb then routes by the shipped
        # template, which is the shipped schema by definition.
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
            # The shipped text could not be compared, which is packaged data
            # this repository wrote, so it is a defect to report and not the
            # person's copy.
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

    Three digests answer it: the one setup RECORDED beside the copy, the copy as
    it is now, and the shipped text as it ships now. A copy that still matches
    the record is the copy setup made, so if the shipped text has moved on the
    library is missing what it gained, and that is the INFO this exists for. A
    copy that differs from the record is the person's, and what the shipped text
    did since is not this check's to raise. With no record, which is every
    library set up before the record existed, the two cannot be told apart and
    the detail says so rather than guessing either way. A record naming a
    template other than the configured one is the other INFO, since the copy
    and the configuration then disagree about which tree this library means.

    IT REPORTS AND NEVER WRITES. The copy is the person's declaration, and a
    section the shipped template gained is theirs to take or leave. It reads
    the shipped template only as a fingerprint the definer computes, never as
    text, so it cannot come to route by it.
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
        # The record carries the one fact that shows the configured name and
        # the copy disagree, and the check above only asserted the name ships.
        # Every verb reads the copy, so the library declares the recorded
        # template's tree whatever the configuration says, and a re-run of
        # setup leaves the copy alone rather than replacing it.
        return Status.INFO, (
            f"the copy was made from the shipped {record.template!r} and "
            f"taxonomy.template now names {named!r}; every verb reads the copy, "
            f"so this library declares the tree of {record.template!r}, and a "
            f"re-run of setup leaves an existing copy alone"
        )
    active = taxonomy.template_fingerprint(active_text)
    # ``named`` is in the shipped set, the check above refused otherwise, so the
    # only way not to read it is packaged data that lists and does not open,
    # which is the damaged install setup reports the same way.
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
        # A NOTE NAMING THE PROCESS, NEVER A PASS (U211). The scan met a live
        # process it could not read, so the absence is unknown and is said as
        # unknown; it is a note rather than a failure because it clears as the
        # process finishes exiting, and every write refuses on its own until it
        # does. A zombie the scan met was skipped and never reaches here.
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
        # S2. An unset pin refuses every database write, and it is never adopted
        # from whatever happens to be installed: a pin the software copies from
        # its own machine refuses nothing, forever.
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


def _check_paths_resolved(inputs: _Inputs) -> Finding:
    """Whether the collection's recorded paths can be read from this machine.

    THE CHECK R-372 ASKED FOR, AND THE FIRST ONE TO READ THE PREFIX MAP. The
    first real My Tags plan reported ok with count 0 over 9937 active rows it
    had skipped, because rekordbox records nearly every row under the drive's
    old name and setup had written no rule, and this report was green beside
    it. Doctor now reads the same ratio the plan refuses on, off a disposable
    copy of the database, so a person is told before the plan rather than by
    reading a zero.

    THE ORDER OF THE QUESTIONS IS WHAT KEEPS THE COPY HONEST. Whether rekordbox
    is running is asked FIRST, through the same seam ``rekordbox.closed``
    answers with, because a copy taken under the live application is torn the
    way a backup taken under it is: it opens, and is missing whatever was mid
    write, and a torn copy's open failure would then be forwarded as a refusal
    naming a snapshot restore against a library that is fine. Whether the
    volume is there is asked SECOND, before anything at the configured path is
    read, for the reason
    the taxonomy check asks it: a leftover mount point holding a stale database
    is the first of the three states ``core/preflight`` exists to tell apart,
    and a survey over it is a report on a disk nobody is using. It is not gated
    on ``required`` the way the trash check is, and the gate was written and
    removed: the routing passes, the rebuild and the convergence report resolve
    recorded paths and are core verbs on every profile, so the question is
    required everywhere and a branch for "nobody asks it" was a branch nothing
    could reach.

    THEN THE ANSWERS, AND "COULD NOT LOOK" IS NOT ONE OF THE GOOD ONES. No file
    at the configured path is INFO, because a fresh library has nothing to
    resolve yet. A copy that would not open is FAIL carrying the open's own
    cause and remedy, since an unanswered question is not a pass. A majority of
    rows under no rule is FAIL under the same slug the plan refuses with, so
    doctor exits under that code and the two surfaces cannot disagree. A
    minority is INFO with the count, which is the state the sitting was left in
    after the rule was typed by hand, 167 of 9937, and a person should see the
    number rather than an unqualified green.
    """
    key, title = "library.paths_resolved", "recorded paths resolve on this machine"
    if inputs.cfg is None:
        return _unchecked(key, title)
    cfg = inputs.cfg
    try:
        running = processes.rekordbox_processes_running(lister=inputs.probes.process_lister)
    except processes.AbsenceUnconfirmed as exc:
        # NO COPY OVER AN ABSENCE NOBODY CONFIRMED (U211), said as unknown and
        # as a note, as rekordbox.closed says the same condition.
        return Finding(
            key=key,
            title=title,
            status=Status.INFO,
            detail=(
                f"whether the collection's rows resolve was not established: "
                f"{exc.cause.message}, so no copy of the database was taken. The "
                f"answer is unknown rather than good"
            ),
        )
    if running:
        # FAIL and not INFO, with the act that unblocks it. The condition is
        # reported by rekordbox.closed as well, and this is not that report
        # repeated: it says this question is unanswered until that one is
        # fixed, which is a different sentence from "the application is open".
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"whether the collection's rows resolve could not be established: "
                f"{', '.join(running)} running, and a copy of the database taken "
                f"under a live application is incomplete, so none was taken. The "
                f"answer is unknown rather than good"
            ),
            remedy=Remedy.QUIT_REKORDBOX,
        )
    unreadable = _library_state_unreadable(inputs, "the database")
    if unreadable is not None:
        return Finding(key=key, title=title, status=Status.INFO, detail=unreadable)
    try:
        totals = inputs.probes.path_survey(cfg)
    except CratekitError as exc:
        cause = exc.cause
        return Finding(
            key=key,
            title=title,
            status=Status.FAIL,
            detail=(
                f"whether the collection's rows resolve could not be established: "
                f"a copy of the database could not be opened, {cause.message}. The "
                f"answer is unknown rather than good, and the live file was not "
                f"touched"
            ),
            remedy=cause.remediation.remedy,
            cause=cause,
        )
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
