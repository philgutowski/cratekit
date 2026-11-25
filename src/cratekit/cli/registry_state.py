"""The verb table, part 1 of 5: setup and the product's own state (KTD7).

Setup, profiles and runs, the row repairs, the write session and its safety
spine, jobs and review.

One literal tuple of ``Entry(...)`` calls, a contiguous slice of the table
(U328). ``cli.registry`` imports it once the names below are bound and
assembles the parts into ``ENTRIES`` in their order, so a verb is read through
``cli.registry``, never from here. A new verb's block is appended to the
last part, ``cli.registry_later``.
"""

from __future__ import annotations

from cratekit.cli.registry import CLOUD_SYNC_UNREADABLE_GATE, REPAIR_CLI_MODULE, Entry, GateSpec

STATE_VERBS: tuple[Entry, ...] = (
    # ── Setup, profiles, and the run's own state (this unit) ────────────────
    Entry(
        name="profile.show",
        summary="show the active profile and which feature modules it switches on",
        module="cratekit.cli.verbs.profile", builder="build", handler_key="profile.show",
        feature_rows=(27,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        doctor_checks=(),
    ),
    Entry(
        name="profile.set", summary="change the profile preset, and nothing else",
        module="cratekit.cli.verbs.profile", builder="build_set", handler_key="profile.set",
        feature_rows=(27,), emits=frozenset({"plan"}), output_schema="plan/1", writes=frozenset(),
        gates=(
            GateSpec(
                name="profile.set.apply", options=("apply", "abort"),
                prompt="Apply this change to module membership?", digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="run.show",
        summary="show a run's state, its outstanding gates, and any pending human action",
        module="cratekit.cli.verbs.runs", builder="build_show", handler_key="run.show",
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="run.decide",
        summary="answer a named gate on a run, from any process and any later session",
        module="cratekit.cli.verbs.runs", builder="build_decide", handler_key="run.decide",
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="run.retire",
        summary="answer abort on every open gate idle past a threshold, after one confirm",
        module="cratekit.cli.verbs.runs", builder="build_retire", handler_key="run.retire",
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        gates=(
            GateSpec(
                name="run.retire.confirm", options=("apply", "abort"),
                prompt="Answer abort, as session, on each of these open gates?",
                #: Ordinary (U170): it writes only run state, only the answer no,
                #: and the digest binds the answer to the gates shown.
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="setup", summary="first-run wizard: library, credentials, taxonomy, profile",
        module="cratekit.cli.setup", builder="build", handler_key="setup", feature_rows=(27,),
        source_scripts=(),
        # Interactive, confined to one module so the static guard on standard
        # input can allow exactly one file.
        interactive=True, emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="doctor", summary="check the environment and report each failure with its fix",
        module="cratekit.cli.doctor", builder="build", handler_key="doctor", feature_rows=(28,),
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="repair.paths",
        summary="propose a name for each file rekordbox would reject, and apply the accepted ones",
        module=REPAIR_CLI_MODULE, builder="build_repair_paths", handler_key="repair.paths",
        feature_rows=(17,), source_scripts=("dj-path-repair",), module_id="repair",
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: Files only (U102): ``--apply`` renames accepted files. The database is
        #: only read, so no cloud sync decision, which a verb must reach to declare.
        writes=frozenset({"files"}), adjudicates=True, destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="repair.paths.confirm", options=("apply", "abort"),
                prompt="Apply these accepted renames?", digest_source="plan",
            ),
        ),
    ),
    # ── A row's rekordbox defaults (R-923) ──────────────────────────────────
    Entry(
        name="repair.rows",
        summary=(
            "give each live library row rekordbox's own defaults where a "
            "column is empty, and its file's inode where the file id is random, so "
            "it loads to a deck; writes no file"
        ),
        module="cratekit.write.row_defaults_cli", builder="build", handler_key="repair.rows",
        # No feature row or source script: the source never created a row.
        # Gated by ``repair``, a corrective pass over rows the library holds.
        module_id="repair", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The row only: ``rb_writer.CONTENT_ROW_DEFAULTS`` where NULL, and
        #: ``rb_writer.FILE_ID_COLUMN`` where the binding minted it (U115).
        writes=frozenset({"db_metadata"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="repair.rows.confirm", options=("apply", "abort"),
                prompt="Give these rows rekordbox's own defaults?",
                #: Explicit (R34): a write to rows of a live library.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The ContentLink probe (A32, R-928) ──────────────────────────────────
    Entry(
        name="repair.link",
        summary=(
            "write chosen values into the row probe columns, ContentLink "
            "and ISRC, of chosen live library rows, the experiment that asks which "
            "column keeps a landed row off a deck; writes no file"
        ),
        module="cratekit.write.row_link_cli", builder="build", handler_key="repair.link",
        # No feature row or source script; gated by ``repair`` as ``repair.rows`` is.
        module_id="repair", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The named rows only, and only the ``rb_writer.ROW_PROBE_COLUMNS`` named.
        writes=frozenset({"db_metadata"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="repair.link.confirm", options=("apply", "abort"),
                prompt="Write these probe values onto these rows?",
                #: Explicit (R34): a write to a row of a live library.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── Playlists numbered 1 to N again (U958) ──────────────────────────────
    Entry(
        name="repair.numbers",
        summary=(
            "number the live rows of every playlist under this product's nodes, and "
            "any named, 1 to N in the order rekordbox shows them, so a removal by "
            "hand takes out the track it was asked to"
        ),
        module="cratekit.write.numbers_cli", builder="build", handler_key="repair.numbers",
        # No feature row or source script: the source never removed a membership.
        # Core, not the ``repair`` module: the gaps it closes were left by core writes.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: each membership row's ``TrackNo`` and its two stamps.
        writes=frozenset({"db_tree"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="repair.numbers.confirm", options=("apply", "abort"),
                prompt="Number these playlists' live rows 1 to N?",
                #: Explicit (R34): a write to the playlists of a live library.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="status", summary="per-source sync state, open runs, unconverged trees, and a glance an app shows",
        module="cratekit.cli.doctor", builder="build_status", handler_key="status",
        feature_rows=(28,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="login", summary="record a provider credential in the OS keychain",
        module="cratekit.cli.verbs.login", builder="build", handler_key="login",
        feature_rows=(27,), source_scripts=("dj-tidal-login",), emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1", doctor_checks=("keychain.reachable",),
    ),
    # ── The write session and its safety spine ──────────────────────────────
    Entry(
        name="session.ack",
        summary="record the backup acknowledgment this destructive session needs",
        module="cratekit.session.cli", builder="build_ack", handler_key="session.ack",
        feature_rows=(12,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        gates=(
            GateSpec(
                name="session.ack.backup", options=("acknowledged", "abort"),
                prompt="Database and music files are backed up; proceed?",
                # Explicit (R34): asserted per session by a named actor.
                explicit=True,
            ),
        ),
        # Landed with ``session.release`` (U49): one module string, one countdown.
    ),
    Entry(
        name="session.release", summary="release a library lock whose holder is gone, explicitly",
        module="cratekit.session.cli", builder="build_release", handler_key="session.release",
        feature_rows=(12,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        gates=(
            GateSpec(
                name="session.release.confirm", options=("release", "abort"),
                prompt="Release the lock held by another installation?", explicit=True,
            ),
        ),
        # The prompt is asked even with no lock recorded, since conformance 3
        # holds every declared gate to firing (U49).
    ),
    Entry(
        name="restore.list",
        summary="list write sessions with their timestamp, workflow, and change summary",
        module="cratekit.session.restore_cli", builder="build_list", handler_key="restore.list",
        feature_rows=(12,), emits=frozenset({"review_set"}), output_schema="review_set/1",
        # Landed (U27); three of the nine conformance properties arm against it.
    ),
    Entry(
        name="restore.run",
        summary="restore a session snapshot, database and coupled state together",
        module="cratekit.session.restore_cli", builder="build_run", handler_key="restore.run",
        feature_rows=(12,), emits=frozenset({"plan"}), output_schema="plan/1",
        writes=frozenset({"db_tree", "db_metadata", "files"}), destructive=True,
        doctor_checks=("library.mounted", "library.identity", "rekordbox.closed"),
        gates=(
            GateSpec(
                name="restore.run.confirm", options=("restore", "abort"),
                prompt="Restore this session, discarding everything after it?", explicit=True,
                digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
        # Landed with its sibling above: one module.
    ),
    Entry(
        name="restore.bare-metal",
        summary="recover the mirror and the database onto a replacement drive",
        module="cratekit.session.restore_cli", builder="build_bare_metal",
        handler_key="restore.bare-metal", feature_rows=(12,), emits=frozenset({"plan"}),
        output_schema="plan/1", writes=frozenset({"files"}), destructive=True,
        doctor_checks=("rekordbox.closed",),
        # U96, a verb of its own because the library volume is gone. The library
        # checks are absent since this verb needs them to fail. No gate: one
        # could not end OK where the library is present, so
        # ``--accept-replacement``, refused without a terminal, is the explicit
        # act. No ``binary.rclone``, which would fail a slim core install; the
        # engine refuses by name instead. ``files``: the database is a copied file.
    ),
    Entry(
        name="converge",
        summary="report, per governed tree, whether declared membership matches the database",
        module="cratekit.cli.converge", builder="build", handler_key="converge",
        feature_rows=(12,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        doctor_checks=("library.mounted", "library.paths_resolved"),
    ),
    Entry(
        name="rebuild",
        summary="rebuild a governed tree's membership from declared sources and library truth",
        module="cratekit.cli.rebuild", builder="build", handler_key="rebuild", feature_rows=(12,),
        argv_builder="rebuild_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", writes=frozenset({"db_tree"}), destructive=True,
        doctor_checks=(
            "library.mounted", "library.identity", "rekordbox.closed", "library.paths_resolved",
        ),
        gates=(
            CLOUD_SYNC_UNREADABLE_GATE,
            GateSpec(
                name="rebuild.accept", options=("accept", "abort"),
                prompt="Accept this tree as it stands? No rebuild can reproduce it.",
                #: Explicit (U219, R34): a named person disposes of a convergence
                #: refusal for a restored tree no rebuild can reproduce.
                explicit=True,
            ),
        ),
    ),
    # The two verbs over ``core.tree_registry`` (R-235). ``writes`` is empty:
    # they write this product's registry file and only read a database copy, so
    # no cloud sync decision. Not destructive, so no backup acknowledgment; the
    # precheck (verified snapshot, Fresh Export) and the explicit gate stand in.
    Entry(
        name="tree.cutover",
        summary="record one tree's cutover from the XML bridge to the database",
        module="cratekit.cli.cutover", builder="build", handler_key="tree.cutover",
        feature_rows=(12,), emits=frozenset({"plan"}), output_schema="plan/1",
        # ``tree.registry`` is not declared: it reports what these verbs record,
        # and an unreadable registry refuses both through the read itself.
        doctor_checks=("library.mounted", "rekordbox.closed"),
        gates=(
            GateSpec(
                name="tree.cutover.approve", options=("approve", "abort"),
                prompt="Record this tree as database native, anchored to this root?",
                # One way: a revert undoes it only until the first native write.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="tree.revert",
        summary="put a cut over tree back on the XML bridge, before its first native write",
        module="cratekit.cli.cutover", builder="build_revert", handler_key="tree.revert",
        feature_rows=(12,), emits=frozenset({"plan"}), output_schema="plan/1",
        doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="tree.revert.approve", options=("revert", "abort"),
                prompt="Put this tree back on the XML bridge?", explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    # ── Jobs ────────────────────────────────────────────────────────────────
    # Under ``cli``, not ``core``: a verb module imports this registry (KTD23, U10).
    Entry(
        name="job.list", summary="list queued, running, blocked, and finished jobs",
        module="cratekit.cli.jobs", builder="build_list", handler_key="job.list",
        feature_rows=(26,), emits=frozenset({"job_state"}), output_schema="job_state/1",
    ),
    Entry(
        name="job.show", summary="show one job, its progress, and the cause behind its state",
        module="cratekit.cli.jobs", builder="build_show", handler_key="job.show",
        feature_rows=(26,), emits=frozenset({"job_state"}), output_schema="job_state/1",
    ),
    Entry(
        name="job.resume", summary="resume an interrupted job without repeating completed work",
        module="cratekit.cli.jobs", builder="build_resume", handler_key="job.resume",
        feature_rows=(26,),
        # The builder is declared because long running work needs one; a resume
        # re-invokes the job's own verb, resolved by ``cli.jobs.argv_for``.
        argv_builder="resume_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1",
    ),
    Entry(
        name="job.cancel", summary="cancel a job; it reports as cancelled rather than as failed",
        module="cratekit.cli.jobs", builder="build_cancel", handler_key="job.cancel",
        feature_rows=(26,), emits=frozenset({"job_state"}), output_schema="job_state/1",
    ),
    # ── Review ──────────────────────────────────────────────────────────────
    # Under ``cli``, not ``core``, for the job verbs' reason (U11).
    Entry(
        name="review.list", summary="list every item awaiting a person's decision",
        module="cratekit.cli.review", builder="build_list", handler_key="review.list",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    Entry(
        name="review.resolve",
        summary="record a verdict on a review item so it is never asked again",
        module="cratekit.cli.review", builder="build_resolve", handler_key="review.resolve",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
)
