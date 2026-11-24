"""The verb table, part 2 of 5: the pipeline from intake to analysis (KTD7).

Intake, tagging and naming, acquisition, routing and the audits, and analysis.

One literal tuple of ``Entry(...)`` calls, a contiguous slice of the table
(U328). ``cli.registry`` imports it once the names below are bound and
assembles the parts into ``ENTRIES`` in their order, so a verb is read through
``cli.registry``, never from here. A new verb's block is appended to the
last part, ``cli.registry_later``.
"""

from __future__ import annotations

from cratekit.cli.registry import CLOUD_SYNC_UNREADABLE_GATE, Entry, GateSpec

PIPELINE_VERBS: tuple[Entry, ...] = (
    # ── Intake ──────────────────────────────────────────────────────────────
    Entry(
        name="intake.set",
        summary="identify a set recording, or a mix URL fetched first, and resolve its tracks",
        module="cratekit.intake.cli", builder="build_set", handler_key="intake.set",
        feature_rows=(1, 2), source_scripts=("dj-pipeline",), module_id="identify",
        argv_builder="set_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        # The account playlist is a remote write behind its own gate, soft
        # skipped without a provider session (U129).
        writes=frozenset({"xml", "files", "remote"}), adjudicates=True, destructive=True,
        # Doctor fails on exactly what ``recognize.recognition_ready`` refuses on.
        # No ``binary.yt-dlp``: only a mix URL needs it, and refuses without it (U104).
        doctor_checks=(
            "library.mounted", "binary.ffmpeg", "binary.ffprobe", "credential.recognition",
            "credential.provider",
        ),
        gates=(
            GateSpec(
                name="intake.set.account.confirm", options=("apply", "abort"),
                prompt="Save this set as a private playlist on the streaming account?",
                # Explicit (R34): an account write.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="intake.identify",
        summary="identify the tracks in a set recording or a mix URL and stop; acquire nothing",
        module="cratekit.intake.cli", builder="build_identify", handler_key="intake.identify",
        feature_rows=(5,), source_scripts=("dj-setid",), module_id="identify",
        # A version the library may hold is offered for review (U103). Its own
        # tracklist file is no write surface, as for ``intake missing``.
        adjudicates=True, emits=frozenset({"match"}), output_schema="match/1",
        # The library is asked, so doctor must require it.
        doctor_checks=(
            "library.mounted", "binary.ffmpeg", "binary.ffprobe", "credential.recognition",
        ),
    ),
    Entry(
        name="intake.playlist", summary="import a streaming playlist's tracks into the library",
        module="cratekit.intake.cli", builder="build_playlist", handler_key="intake.playlist",
        feature_rows=(3, 35), argv_builder="playlist_argv", long_running=True,
        emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"xml", "files"}), adjudicates=True, destructive=True,
        doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="intake.missing",
        summary=(
            "write the list acquire download reads from the missing tracks of a "
            "finished intake job, a whole sync pass, or a text list searched on "
            "the provider"
        ),
        module="cratekit.intake.missing_cli", builder="build_missing",
        handler_key="intake.missing", feature_rows=(3, 35),
        # ``--list`` offers candidates and version questions for review (U79).
        adjudicates=True,
        # ``diagnostic/1``: the human renderer shows checks, and a person needs
        # the list's path and the download command (R-400).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # No write surface, so not destructive: two new files, never a replace.
        # The library is asked again, so doctor requires it (R-502).
        doctor_checks=("library.mounted",),
    ),
    Entry(
        name="intake.file", summary="ingest one audio file already on disk",
        module="cratekit.intake.file_cli", builder="build_file", handler_key="intake.file",
        feature_rows=(4,), emits=frozenset({"plan"}), output_schema="plan/1",
        #: On a database native intake tree the file becomes a content row and a
        #: batch playlist (R-770); on the bridge, an intake file.
        writes=frozenset({"xml", "files", "db_tree"}), destructive=True,
        #: The database checks hold for the native medium only.
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            # A content row, answered by a separate recorded act (R34, R-770).
            GateSpec(
                name="intake.file.native", options=("apply", "abort"),
                prompt="Add this file to the collection?", explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="intake.shelve",
        summary=(
            "file an imported batch folder into the processed tree, by year and date, "
            "and point its rows at it"
        ),
        module="cratekit.intake.shelve_cli", builder="build_shelve", handler_key="intake.shelve",
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: One folder rename and the path column of its rows, never the tree (U154).
        writes=frozenset({"files", "db_metadata"}), destructive=True,
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            # A path write on the collection, answered by a recorded act (R34).
            GateSpec(
                name="intake.shelve.native", options=("apply", "abort"),
                prompt="Move these batches into the processed tree and point their rows at it?",
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="tag.folder", summary="tag a folder of audio with genre and album art",
        module="cratekit.tagging.cli", builder="build", handler_key="tag.folder",
        feature_rows=(8,), source_scripts=("dj-tag-folder",), argv_builder="tag_argv",
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"files"}), destructive=True, doctor_checks=("binary.ffmpeg",),
    ),
    Entry(
        name="tag.retag",
        summary="replace a genre too coarse to be a final tag with a specific one",
        module="cratekit.tagging.retag_cli", builder="build", handler_key="tag.retag",
        feature_rows=(18,),
        #: No source script: the two cut genre migrations stay cut (``CUT.md``).
        source_scripts=(),
        #: Gated by ``repair``: correcting metadata the library already holds is
        #: an opt in second job, as ``repair.paths`` is for locations.
        module_id="repair", argv_builder="retag_argv", long_running=True,
        emits=frozenset({"job_state"}), output_schema="job_state/1",
        #: The file only (R-246): the row follows by ``tag.rows``, which the run
        #: names. No database is opened, so no cloud sync decision.
        writes=frozenset({"files"}), adjudicates=True, destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="tag.retag.confirm", options=("apply", "abort"),
                prompt="Correct the genre on these files?",
                #: Explicit because the verb queues: the recorded act gives the
                #: detached child a run to name (``test_queued_resume_contract``).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="name.apply", summary="rename files and rewrite name fields from the naming template",
        module="cratekit.write.naming_cli", builder="build", handler_key="name.apply",
        feature_rows=(11,), source_scripts=("dj-pad-camelot",), emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: Files only (U39). The database is only read, to hold back referenced
        #: files (U67), so no cloud sync decision. A partial run answers
        #: ``rename-incomplete`` on the plan surface (R-172).
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.pins", "library.paths_resolved"),
        gates=(
            GateSpec(
                name="name.apply.confirm", options=("apply", "abort"),
                prompt="Apply these renames?", digest_source="plan",
            ),
        ),
        #: The naming half of intake; U21 landed only its per field policy.
    ),
    # ── Acquisition ─────────────────────────────────────────────────────────
    Entry(
        name="acquire.download", summary="acquire matched tracks through the configured adapter",
        module="cratekit.acquire.cli", builder="build", handler_key="acquire.download",
        feature_rows=(6, 7), argv_builder="download_argv", long_running=True,
        emits=frozenset({"job_state"}), output_schema="job_state/1", writes=frozenset({"files"}),
        destructive=True, doctor_checks=("credential.provider", "binary.ffmpeg"),
        # Landed (U42). No gate, argued in ``cratekit.acquire.cli``'s docstring.
    ),
    Entry(
        name="acquire.audit",
        summary="report existing files that do not match the lossless policy",
        module="cratekit.acquire.cli", builder="build_audit", handler_key="acquire.audit",
        feature_rows=(7,), emits=frozenset({"review_set"}), output_schema="review_set/1",
        # Landed (U42), beside the verb above.
    ),
    Entry(
        name="acquire.fallback",
        summary=(
            "search SoundCloud and YouTube for a list's missing tracks and offer "
            "what they hold for review; downloads nothing"
        ),
        module="cratekit.acquire.fallback_cli", builder="build", handler_key="acquire.fallback",
        feature_rows=(7,),
        # Offers candidates and version questions for review (U80).
        adjudicates=True,
        # ``diagnostic/1``, for ``intake.missing``'s reason.
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # NO WRITE SURFACE: it writes review items and nothing else.
        doctor_checks=("library.mounted", "binary.yt-dlp"),
    ),
    Entry(
        name="acquire.fallback-fetch",
        summary=(
            "download the second source candidates accepted in review into staging, "
            "marked lossy and tagged from the list's row"
        ),
        module="cratekit.acquire.fallback_cli", builder="build_fetch",
        handler_key="acquire.fallback-fetch", feature_rows=(7,), argv_builder="fetch_argv",
        long_running=True,
        # Resolving the list raises version questions, as ``acquire.fallback`` (U81).
        adjudicates=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "binary.yt-dlp", "binary.ffmpeg"),
        # No gate: it adds files to staging, each chosen in review.
    ),
    Entry(
        name="acquire.bandcamp",
        summary=(
            "list the Bandcamp account's purchases, newest first, each with what "
            "the library already owns; downloads nothing"
        ),
        module="cratekit.acquire.bandcamp_cli", builder="build", handler_key="acquire.bandcamp",
        feature_rows=(6,),
        # A plan a person reads, so the diagnostic surface (U176).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # No write surface: it only reads.
        doctor_checks=("library.mounted", "keychain.reachable"),
    ),
    Entry(
        name="acquire.bandcamp-fetch",
        summary=(
            "download the Bandcamp purchases the library does not own into a "
            "batch folder under download staging, what it owns held back"
        ),
        module="cratekit.acquire.bandcamp_cli", builder="build_fetch",
        handler_key="acquire.bandcamp-fetch", feature_rows=(6,), argv_builder="fetch_argv",
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "keychain.reachable"),
        # No gate: it adds owned purchases to its own staging folder.
    ),
    Entry(
        name="match.run",
        summary="resolve an external list against the library: matched, needs review, or missing",
        module="cratekit.acquire.match_cli", builder="build", handler_key="match.run",
        emits=frozenset({"match"}), output_schema="match/1", adjudicates=True,
    ),
    # ── Routing and audits ──────────────────────────────────────────────────
    Entry(
        name="route.inbox",
        summary="route the intake folder into the declared taxonomy, or an export's with --export",
        module="cratekit.write.routing_cli", builder="build_inbox", handler_key="route.inbox",
        feature_rows=(14,), source_scripts=("dj-sort-inbox",), emits=frozenset({"plan"}),
        output_schema="plan/1",
        # ``--export`` writes a new file beside an export for a bridge tree (U86).
        writes=frozenset({"db_tree", "xml"}), destructive=True,
        taxonomy_terms=("inbox", "genre_energy"),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="route.inbox.apply", options=("apply", "abort"),
                prompt="Apply this routing plan to the library?", digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="route.unplaced",
        summary=(
            "find tracks in the collection that no governed tree places, "
            "or place an export's with --export"
        ),
        module="cratekit.write.routing_cli", builder="build_unplaced",
        handler_key="route.unplaced", feature_rows=(14,), source_scripts=("dj-sort-unplaced",),
        emits=frozenset({"plan"}), output_schema="plan/1",
        # The database is only read (R-313), so no database surface, not
        # destructive, no cloud sync decision. ``--export`` writes a new file
        # beside the export (U91), so ``xml``. The pins stay: a read checks them.
        writes=frozenset({"xml"}), taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted", "rekordbox.pins", "library.paths_resolved"),
    ),
    Entry(
        name="route.resort",
        summary=(
            "add already-routed tracks to their new place after a genre or energy "
            "change, additive, the old membership stays and is named"
        ),
        module="cratekit.write.routing_cli", builder="build_resort", handler_key="route.resort",
        feature_rows=(13,), source_scripts=("dj-resort-energy", "dj-resort-genre"),
        argv_builder="resort_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", writes=frozenset({"db_tree"}), destructive=True,
        taxonomy_terms=("genre_energy", "low", "med", "high"),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="route.resort.apply", options=("apply", "abort"),
                prompt="Add these tracks to the routing tree?",
                #: Explicit, for ``tag.retag.confirm``'s reason (U219); the plan
                #: digest lets a rehearsal hold the live run to it.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    Entry(
        name="audit.coverage", summary="report tracks the governed trees do not cover",
        module="cratekit.cli.reports", builder="build_coverage", handler_key="audit.coverage",
        feature_rows=(14,), source_scripts=("dj-audit-genres",), emits=frozenset({"diagnostic"}),
        output_schema="diagnostic/1", taxonomy_terms=("genre_energy",),
    ),
    Entry(
        name="audit.duplicates",
        summary="review-gated duplicate audit; never deletes, remembers intentional alternates",
        module="cratekit.cli.reports", builder="build_duplicates", handler_key="audit.duplicates",
        feature_rows=(15,), source_scripts=("dj-audit-genres",), module_id="duplicates",
        emits=frozenset({"review_set"}), output_schema="review_set/1", adjudicates=True,
    ),
    Entry(
        name="report.library",
        summary="read-only library statistics: genres, tempo spread, tree shape, gaps",
        module="cratekit.cli.reports", builder="build_library", handler_key="report.library",
        source_scripts=("dj-scan-playlists",), module_id="reports",
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="report.intake-aging", summary="report intake items by age so stale ones are visible",
        module="cratekit.cli.reports", builder="build_intake_aging",
        handler_key="report.intake-aging", feature_rows=(20,),
        source_scripts=("dj-inbox-rotation",), module_id="reports",
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1", taxonomy_terms=("inbox",),
    ),
    # ── Analysis ────────────────────────────────────────────────────────────
    Entry(
        name="analyze.run", summary="analyse audio for tempo, drift, energy and vocals",
        module="cratekit.analysis.cli", builder="build", handler_key="analyze.run",
        feature_rows=(9,), module_id="analysis", extras="analysis",
        extras_modules=("librosa", "numpy", "scipy"), argv_builder="analyze_argv",
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        writes=frozenset({"files"}), destructive=True, doctor_checks=("binary.ffmpeg",),
    ),
    Entry(
        name="analyze.calibrate",
        summary="calibrate an analysis threshold against the library's own data",
        module="cratekit.analysis.cli", builder="build_calibrate", handler_key="analyze.calibrate",
        feature_rows=(9, 10), source_scripts=("dj-energy-calibrate", "dj-vocal-calibrate"),
        module_id="analysis", extras="analysis", extras_modules=("librosa", "numpy", "scipy"),
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # Library scoped state files need the library, but are not ``writes``,
        # which names library material. ffmpeg decodes an M4A (U263).
        doctor_checks=("library.mounted", "binary.ffmpeg"),
    ),
    Entry(
        name="analyze.validate", summary="score the analysers against labelled ground truth",
        module="cratekit.analysis.cli", builder="build_validate", handler_key="analyze.validate",
        feature_rows=(9,), source_scripts=("dj-analyze-validate",), module_id="analysis",
        extras="analysis", extras_modules=("librosa", "numpy", "scipy"),
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="analyze.restamp",
        summary="re-stamp analysed values across the back catalogue after a recalibration",
        module="cratekit.analysis.cli", builder="build_restamp", handler_key="analyze.restamp",
        feature_rows=(9,), source_scripts=("energy_restamp", "energy_rerate"),
        module_id="analysis", extras="analysis", extras_modules=("librosa", "numpy", "scipy"),
        argv_builder="restamp_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", writes=frozenset({"files", "db_metadata"}), destructive=True,
        # ffmpeg decodes what libsndfile cannot open, an M4A (U263).
        doctor_checks=("library.mounted", "rekordbox.pins", "binary.ffmpeg"),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
    ),
    Entry(
        name="analyze.vocals", summary="score tracks for vocal prominence and stamp the result",
        module="cratekit.vocals.cli", builder="build", handler_key="analyze.vocals",
        feature_rows=(10,), source_scripts=("dj-vox-backfill", "dj-vocal-restamp"),
        module_id="vocals", extras="vocals", extras_modules=("torch", "panns_inference"),
        argv_builder="vocals_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", writes=frozenset({"files"}), destructive=True,
        taxonomy_terms=("with_vox",), doctor_checks=("binary.ffmpeg",),
    ),
    Entry(
        name="metadata.mytags-vocals",
        summary="mirror vocal scores into library tag categories on existing rows",
        module="cratekit.write.metadata_cli", builder="build_mytags_vocals",
        handler_key="metadata.mytags-vocals", feature_rows=(10,),
        source_scripts=("dj-vocal-mytags",), module_id="vocals", emits=frozenset({"plan"}),
        output_schema="plan/1", writes=frozenset({"db_metadata"}), destructive=True,
        taxonomy_terms=("with_vox",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            # The ratio the verb refuses on, unmapped rows tag nothing (R-372).
            "library.paths_resolved",
        ),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
        #: My Tags, not content columns, so U21's per field policy does not apply.
    ),
)
