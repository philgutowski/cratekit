"""The verb table, part 3 of 5: sync and the labels (KTD7).

The sync pass and its schedule, the label registry and its sweeps, and a
label's playlists on the account.

One literal tuple of ``Entry(...)`` calls, a contiguous slice of the table
(U328). ``cli.registry`` imports it once the names below are bound and
assembles the parts into ``ENTRIES`` in their order, so a verb is read through
``cli.registry``, never from here. A new verb's block is appended to the
last part, ``cli.registry_later``.
"""

from __future__ import annotations

from cratekit.cli.registry import Entry, GateSpec

SYNC_VERBS: tuple[Entry, ...] = (
    # ── Sync ────────────────────────────────────────────────────────────────
    Entry(
        name="sync.all",
        summary=(
            "queue each enabled source's own increment under one intake run; "
            "label releases are left to crate label sync"
        ),
        module="cratekit.sync.cli", builder="build_all", handler_key="sync.all",
        feature_rows=(25,), source_scripts=("dj-sync",),
        # Not long running: each source queues under its own key (U61, R-203).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        gates=(
            # ``sync.favorites.confirm``'s question, named for this run's verb;
            # ``Gates.hand_off`` carries the answer to the favourites job.
            GateSpec(
                name="sync.all.favorites.confirm", options=("sync", "abort"),
                prompt="Heart matching tracks on the streaming service? This never removes a heart.",
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="sync.land",
        summary=(
            "take a sync pass to its landing in one verb: the pass, its intake "
            "jobs, the missing list, the download and the tail, stopping at the "
            "landing's gate"
        ),
        module="cratekit.cli.sync_land", builder="build", handler_key="sync.land",
        feature_rows=(25,),
        # Not long running: each job it drives queues under its own verb (U152).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # The files its steps write. No database write: the landing stops at
        # its own explicit gate.
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "credential.provider"),
        gates=(
            # Asked only when the vocal model cannot score (U181). Ordinary:
            # it writes nothing the pass would not, so ``-d`` answers it.
            GateSpec(
                name="sync.land.without-vocals", options=("go", "stop"),
                prompt=(
                    "Take the pass although the vocal model cannot score here, so "
                    "every row it lands carries no voxlevel and no vox My Tag?"
                ),
            ),
        ),
    ),
    Entry(
        name="sync.night",
        summary=(
            "run the sync pass unattended, for a schedule overnight: refuses beside "
            "rekordbox, a running job or another pass, holds the night's provider "
            "budget, answers no gate and stops at the landing's gate"
        ),
        module="cratekit.cli.sync_night", builder="build", handler_key="sync.night",
        feature_rows=(25,),
        # Not long running, for ``sync.land``'s reason (U293).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # ``sync land``'s files. No gate: the landing waits at its own gate.
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "credential.provider"),
    ),
    # The night pass as a launchd agent (U295), core and macOS only by refusal.
    # No write surface and not destructive: only the agent's plist and log are
    # touched. No gate: every limit is the night verb's.
    Entry(
        name="schedule.install",
        summary=(
            "install the nightly run of crate sync night as a launchd agent of your "
            "own on macOS, replacing one already installed"
        ),
        module="cratekit.cli.schedule", builder="build_install", handler_key="schedule.install",
        feature_rows=(25,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="schedule.show",
        summary=(
            "show the nightly run's schedule: installed or not, its time, the crate "
            "it runs, whether launchd has it loaded and the last night's line"
        ),
        module="cratekit.cli.schedule", builder="build_show", handler_key="schedule.show",
        feature_rows=(25,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="schedule.remove",
        summary="unload the nightly run's launchd agent and delete it; nothing installed is a no op",
        module="cratekit.cli.schedule", builder="build_remove", handler_key="schedule.remove",
        feature_rows=(25,), emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="sync.bandcamp",
        summary=(
            "take new Bandcamp purchases to their landing in one verb: the plan, the "
            "fetch tagged by label, the tail and a rehearsal, stopping at the "
            "landing's gate"
        ),
        module="cratekit.cli.sync_bandcamp", builder="build", handler_key="sync.bandcamp",
        feature_rows=(6,),
        # Not long running, for ``sync.land``'s reason (U179).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # The files its steps write. No database write: the rehearsal uses a
        # copy, and the landing stops at its own explicit gate.
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "rekordbox.closed", "keychain.reachable"),
    ),
    Entry(
        name="sync.labels",
        # Retired (U109), kept so a sweep queued earlier can resume with
        # ``--job``; otherwise it refuses ``verb-retired``.
        summary=(
            "resume a labels sweep queued before crate label sync replaced it; "
            "retired, it queues nothing new"
        ),
        module="cratekit.label.cli", builder="build_sync", handler_key="sync.labels",
        feature_rows=(21,), source_scripts=("dj-label-batch",), module_id="labels",
        argv_builder="sync_labels_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", writes=frozenset({"xml", "files"}), adjudicates=True,
        destructive=True, doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="sync.favorites",
        summary="heart the library's favourites on the streaming service; add-only, never un-hearts",
        module="cratekit.favorites.cli", builder="build_sync", handler_key="sync.favorites",
        feature_rows=(24,), source_scripts=("dj-favorites",), module_id="favorites",
        argv_builder="sync_favorites_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1",
        # The account only (R-424): it reads an export and colours no row; the
        # outbound ledger is not ``files``, as for ``export.playlist``. Kept
        # destructive, an account write nobody can roll back, pending a ruling.
        writes=frozenset({"remote"}), adjudicates=True, destructive=True,
        # No rekordbox check: the database is never opened. ``library.mounted``
        # stays because the outbound ledger is library scoped.
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="sync.favorites.confirm", options=("sync", "abort"),
                prompt="Heart matching tracks on the streaming service? This never removes a heart.",
                explicit=True, digest_source="plan",
            ),
        ),
        # Landed (U33, R-130).
    ),
    Entry(
        name="label.registry",
        summary="list, add, and remove favourite labels, and adopt accepted harvested ones",
        module="cratekit.label.cli", builder="build_registry", handler_key="label.registry",
        feature_rows=(21,), source_scripts=("dj-label-batch",), module_id="labels",
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
    ),
    Entry(
        name="label.import", summary="bring one label's catalogue into the library",
        module="cratekit.label.cli", builder="build_import", handler_key="label.import",
        feature_rows=(22,), source_scripts=("dj-label-library",), module_id="labels",
        argv_builder="label_import_argv", long_running=True, emits=frozenset({"job_state"}),
        output_schema="job_state/1", writes=frozenset({"xml", "files"}), adjudicates=True,
        destructive=True, doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="label.approved",
        summary=(
            "write the list acquire download reads from the label releases "
            "accepted in review"
        ),
        module="cratekit.label.approved_cli", builder="build_approved",
        handler_key="label.approved", feature_rows=(22,), module_id="labels",
        # ``diagnostic/1``, for ``intake.missing``'s reason (R-402).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # Another version the library holds is offered for review.
        adjudicates=True,
        # No write surface, as for ``intake.missing``.
        doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="label.held",
        summary=(
            "list the releases the label genre gate is holding back, or return "
            "one to review"
        ),
        module="cratekit.label.held_cli", builder="build_held", handler_key="label.held",
        feature_rows=(21,), module_id="labels",
        # ``diagnostic/1``, since the renderer shows checks (R-798).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # ``return`` files a held release under the sweep's own key.
        adjudicates=True,
        # No write surface: the review database is this product's own record.
        doctor_checks=("library.mounted",),
    ),
    Entry(
        name="label.sync",
        summary=(
            "ask, label by label, about the releases new since each label was "
            "last asked, record each answer, then download what was answered for "
            "behind one gate"
        ),
        # A CLI module in front of ``label.sync_cli`` (U190), since only a CLI
        # module may reach the chain ``sync land`` runs.
        module="cratekit.cli.label_sync", builder="build_sync", handler_key="label.sync",
        feature_rows=(21,), module_id="labels",
        # Interactive (U107), reading only through ``cli/prompt.py``;
        # ``--next`` and ``--answer`` keep it scriptable.
        interactive=True,
        # ``diagnostic/1``, for ``label.held``'s reason.
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # It files, accepts, supersedes and withholds review items.
        adjudicates=True,
        # The go writes a list and lands downloads in staging, so it is
        # destructive (U108, KTD24).
        writes=frozenset({"files"}), destructive=True,
        doctor_checks=("library.mounted", "credential.provider"),
        gates=(
            GateSpec(
                name="label.sync.confirm", options=("apply", "abort"),
                prompt="Download every release the saved answers took?",
                #: Explicit: starting an hours long unattended download is its
                #: own recorded act, never one more flag.
                explicit=True,
                #: Over the summary, so an answer saved later makes it stale.
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="label.judge",
        summary=(
            "judge the label releases waiting in review by their label's kind, "
            "and hold the ones the genre gate would not have filed"
        ),
        module="cratekit.label.judge_cli", builder="build_judge", handler_key="label.judge",
        feature_rows=(21,), module_id="labels", argv_builder="label_judge_argv",
        # Queued, so a pass over thousands of paced reads resumes (R-815).
        long_running=True, emits=frozenset({"job_state"}), output_schema="job_state/1",
        # It moves releases into a hold and stamps the rest.
        adjudicates=True,
        # No write surface, on ``label.held``'s reasoning.
        doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="label.artists",
        summary=(
            "give the open label releases whose artist reads as a provider "
            "object address the artist's name"
        ),
        module="cratekit.label.artists_cli", builder="build_artists", handler_key="label.artists",
        feature_rows=(21,), module_id="labels",
        # ``diagnostic/1``, for ``label.held``'s reason (R-840).
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # Not adjudicating: it only names an open item's artist. No write
        # surface, on ``label.held``'s reasoning. Not queued: a rerun asks only
        # what the last left.
        doctor_checks=("library.mounted", "credential.provider"),
    ),
    Entry(
        name="label.harvest",
        summary="harvest the labels behind a playlist's tracks; imports nothing",
        module="cratekit.label.cli", builder="build_harvest", handler_key="label.harvest",
        feature_rows=(22,), module_id="labels", emits=frozenset({"review_set"}),
        output_schema="review_set/1", adjudicates=True,
    ),
    # ── A label's folder of year playlists on the account (R-835) ───────────
    Entry(
        name="label.playlists",
        summary=(
            "build a followed label's folder of private year playlists on the "
            "streaming account; adds, never removes, and never adds a track the "
            "library removed through delete review"
        ),
        module="cratekit.label.playlists_cli", builder="build_playlists",
        handler_key="label.playlists", feature_rows=(23,), source_scripts=("dj-label",),
        module_id="labels", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only. Not destructive, as ``export.playlist``: every
        #: write adds. The outbound ledger is not a declared surface.
        writes=frozenset({"remote"}), doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="label.playlists.confirm", options=("apply", "abort"),
                prompt="Build this label's folder of year playlists on the streaming account?",
                # Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
            # A build over ``playlists_cli.FULL_BUILD_CALLS`` provider calls
            # stops here first, since it spends the provider's patience (U191).
            GateSpec(
                name="label.playlists.crawl", options=("crawl", "abort"),
                prompt="Read this label's whole catalogue from the provider?", explicit=True,
                digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="label.mark",
        summary="record the year playlists of a label whose batch has landed as taken",
        module="cratekit.label.mark_cli", builder="build_mark", handler_key="label.mark",
        feature_rows=(23,), module_id="labels", emits=frozenset({"plan"}), output_schema="plan/1",
        #: No write surface (U242): the account is read, and the mark is held
        #: in ``sync mark``'s record, this product's own state.
        writes=frozenset(), doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="label.mark.confirm", options=("apply", "abort"),
                prompt="Record these year playlists as taken?",
                # Explicit, as ``sync.mark``'s is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── Taking dropped tracks off a label's year playlists (R-836) ──────────
    Entry(
        name="label.prune",
        summary=(
            "take the tracks the genre gate holds, the catalogue no longer "
            "confirms, or the library removed through delete review off the year "
            "playlists this product made for a label"
        ),
        module="cratekit.label.prune_cli", builder="build_prune", handler_key="label.prune",
        feature_rows=(23,), module_id="labels", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only: ``remove_tracks`` on a year playlist this product
        #: created. Destructive because it takes something away.
        writes=frozenset({"remote"}), destructive=True, doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="label.prune.confirm", options=("apply", "abort"),
                prompt="Take these tracks off this label's year playlists on the streaming account?",
                # Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
)
