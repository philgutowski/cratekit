"""The verb table, part 4 of 5: adoption, deletion, export and the utilities (KTD7).

Adoption, deletion and its tombstones, export, and the standalone utilities:
the set builder, mastering, backup and the skills.

One literal tuple of ``Entry(...)`` calls, a contiguous slice of the table
(U328). ``cli.registry`` imports it once the names below are bound and
assembles the parts into ``ENTRIES`` in their order, so a verb is read through
``cli.registry``, never from here. A new verb's block is appended to the
last part, ``cli.registry_later``.
"""

from __future__ import annotations

from cratekit.cli.registry import CLOUD_SYNC_UNREADABLE_GATE, Entry, GateSpec

MODULE_VERBS: tuple[Entry, ...] = (
    # ── Adoption, deletion, export, standalone utilities ────────────────────
    Entry(
        name="adopt.scan",
        summary="scan an existing library and propose a mapping into the taxonomy",
        # Its own module, apart from ``adopt.apply`` (``ADOPT_APPLY_CLI_UNIT``).
        module="cratekit.adopt.scan_cli", builder="build", handler_key="adopt.scan",
        feature_rows=(34,), module_id="adoption", argv_builder="adopt_scan_argv",
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted", "library.paths_resolved"),
    ),
    Entry(
        name="adopt.apply", summary="apply an approved adoption plan, incrementally and resumably",
        module="cratekit.adopt.apply_cli", builder="build", handler_key="adopt.apply",
        feature_rows=(34,), module_id="adoption", argv_builder="adopt_apply_argv",
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"db_tree", "db_metadata"}), destructive=True,
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="adopt.apply.approve", options=("approve", "abort"),
                prompt="Apply this adoption plan to the library?",
                # Explicit (R34), as the backup acknowledgment is.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # A verb that removes a membership (R-758), not a mode of the additive
    # ``route.resort``, since gates are declared per verb. Decided over
    # ``adopt.apply``'s plan and census (R-780).
    Entry(
        name="adopt.move",
        summary=(
            "move each track from the energy or style sub it holds to the one "
            "its own file names, and a row tag set moved out of its old genre "
            "folder into the new one, adding before it removes"
        ),
        module="cratekit.adopt.move_cli", builder="build", handler_key="adopt.move",
        feature_rows=(13,), module_id="adoption", argv_builder="adopt_move_argv",
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"db_tree"}), destructive=True,
        taxonomy_terms=("genre_energy", "low", "med", "high"),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="adopt.move.approve", options=("approve", "abort"),
                prompt=(
                    "Move these tracks, adding each to its new sub and then "
                    "removing it from the old one?"
                ),
                # Explicit (R34): a removal takes something away.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── Deletion: one surface, two modules ──────────────────────────────────
    # Two modules so ``tombstone.list``, which writes nothing, did not wait on
    # the destructive verb (R36). ``delete.review`` runs inline, not queued
    # (U60, R-149): the person who confirmed the plan watches the files go.
    Entry(
        name="delete.review",
        summary="review tracks removed from the collection and trash the confirmed files",
        module="cratekit.deletion.cli", builder="build_review", handler_key="delete.review",
        feature_rows=(37,), module_id="deletion", emits=frozenset({"review_set"}),
        output_schema="review_set/1", adjudicates=True, destructive=True,
        writes=frozenset({"files"}),
        # ``library.trash`` only here, the one verb that trashes a file (R35);
        # a precondition, since the pass would otherwise refuse after the confirm.
        doctor_checks=(
            "library.mounted", "library.identity", "library.trash", "rekordbox.closed",
            "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="delete.review.confirm", options=("trash", "abort"),
                prompt="Move these files to the system Trash?", explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="tombstone.list",
        summary="list and revoke tombstones so a suppressed version is visible",
        module="cratekit.deletion.tombstone_cli", builder="build_tombstones",
        handler_key="tombstone.list", feature_rows=(37,), module_id="deletion",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    Entry(
        name="export.playlist", summary="export a library playlist to a streaming service",
        module="cratekit.export.cli", builder="build", handler_key="export.playlist",
        feature_rows=(36,), module_id="export", argv_builder="export_argv", long_running=True,
        emits=frozenset({"job_state"}), output_schema="job_state/1", writes=frozenset({"remote"}),
        doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="export.playlist.confirm", options=("export", "abort"),
                prompt="Write this playlist to the streaming service?", explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="export.prune",
        summary=(
            "take the tracks no longer in a library playlist off the remote "
            "playlist it was exported to"
        ),
        module="cratekit.export.prune_cli", builder="build_prune", handler_key="export.prune",
        feature_rows=(36,), module_id="export", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only: ``remove_tracks`` on a playlist ``export.playlist``
        #: made. Destructive, for ``label.prune``'s reason.
        writes=frozenset({"remote"}), destructive=True, doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="export.prune.confirm", options=("apply", "abort"),
                prompt="Take these tracks off the remote playlist on the streaming service?",
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── A set as a playlist on the account, and its archive (R-837) ─────────
    Entry(
        name="export.set",
        summary=(
            "make an identified set or a typed tracklist a private playlist on the "
            "streaming account; adds, never removes"
        ),
        module="cratekit.export.set_cli", builder="build_set", handler_key="export.set",
        feature_rows=(36,), module_id="export", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only, and not destructive, as ``export.playlist``: a
        #: private playlist is created and filled. ``--rename`` (U140) retitles
        #: one this product made to its INSPIRATION name and takes nothing away.
        writes=frozenset({"remote"}),
        # The library: the backfill and the rename read the database (U129).
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="export.set.confirm", options=("apply", "abort"),
                prompt="Make this set a private playlist on the streaming account?",
                # Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
            GateSpec(
                name="export.set.rename", options=("apply", "abort"),
                prompt=(
                    "Rename this set's playlist on the streaming account to its "
                    "INSPIRATION playlist's name, and record the new name?"
                ),
                # Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="export.archive",
        summary=(
            "file a downloaded set's playlist in Downloaded Sets <year> on the "
            "streaming account, and record it as taken"
        ),
        module="cratekit.export.set_cli", builder="build_archive", handler_key="export.archive",
        feature_rows=(36,), module_id="export", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only: the playlist moves into the year's folder (U142),
        #: held as taken in ``sync mark``'s record (U242). Destructive: the
        #: move changes where a person finds it.
        writes=frozenset({"remote"}), destructive=True,
        # The library: the backfill reads the database (U129).
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="export.archive.confirm", options=("apply", "abort"),
                prompt=(
                    "File this set playlist in Downloaded Sets for its year on the "
                    "streaming account?"
                ),
                # Explicit, as ``label.mark``'s is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="setbuild", summary="build a short set or transition around an anchor track",
        module="cratekit.setbuilder.cli", builder="build", handler_key="setbuild",
        feature_rows=(29,), source_scripts=("dj-set-builder",), module_id="setbuilder",
        emits=frozenset({"plan"}), output_schema="plan/1",
        # Landed (U43). Its index cache is library state, not ``writes``, as
        # for ``analyze.calibrate`` (R-188), so the verb is not destructive.
    ),
    Entry(
        name="master",
        summary="master a recorded set to a consistent loudness without touching the source",
        module="cratekit.master.cli", builder="build", handler_key="master", feature_rows=(30,),
        module_id="mastering",
        # Named so parity sees what the predecessor did (U105, R-193).
        source_scripts=("master_set.sh",), argv_builder="master_argv", long_running=True,
        emits=frozenset({"job_state"}), output_schema="job_state/1", writes=frozenset({"files"}),
        destructive=True, doctor_checks=("binary.ffmpeg",),
        # Landed (U44). No gate: it writes a new file and archives the original,
        # and ``--overwrite`` is itself the explicit act. So ``master_argv``
        # carries no ``--run``.
    ),
    Entry(
        name="backup.run",
        summary="back the library up, and publish the backup age the write session consults",
        module="cratekit.backup.cli", builder="build", handler_key="backup.run",
        feature_rows=(31,), source_scripts=("backup.sh",), module_id="backup",
        argv_builder="backup_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", doctor_checks=("library.mounted", "binary.rclone"),
        # Landed (U45). No gate and no write surface, argued in the shell's
        # docstring: it only adds a mirror and an archive. So no ``--run``.
    ),
    Entry(
        name="skills.install", summary="install the operator skills that ship with the package",
        module="cratekit.skills.cli", builder="build", handler_key="skills.install",
        feature_rows=(33,), module_id="skills", emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1",
        # Landed (U28). The module path here is the one the dispatcher imports.
    ),
)
