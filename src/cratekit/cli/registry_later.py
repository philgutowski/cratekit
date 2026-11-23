"""The verb table, part 5 of 5: the blocks appended since (KTD7).

Each block a unit appended after the table was first laid out by surface, in
the order it landed, from the rest of the review surface (U11) on.

One literal tuple of ``Entry(...)`` calls, a contiguous slice of the table
(U328). ``cli.registry`` imports it once the names below are bound and
assembles the parts into ``ENTRIES`` in their order, so a verb is read through
``cli.registry``, never from here. A new verb's block is appended to this
part, so concurrent branches conflict, and opens a new part before this one
passes 1,500 lines.
"""

from __future__ import annotations

from cratekit.cli.registry import CLOUD_SYNC_UNREADABLE_GATE, Entry, GateSpec

LATER_VERBS: tuple[Entry, ...] = (
    # ── The rest of the review surface (U11) ────────────────────────────────
    # Appended rather than beside their siblings, so a concurrent branch
    # conflicts textually instead of auto merging unread.
    Entry(
        name="review.show",
        summary="show one review item whole: its payload, its candidates, its verdict",
        module="cratekit.cli.review", builder="build_show", handler_key="review.show",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    Entry(
        name="review.clear", summary="revoke a verdict, so a rejected item is asked about again",
        module="cratekit.cli.review", builder="build_clear", handler_key="review.clear",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    Entry(
        name="review.export", summary="write the queue to a versioned file, verdicts included",
        module="cratekit.cli.review", builder="build_export", handler_key="review.export",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    Entry(
        name="review.import",
        summary="take an exported queue back in, never overwriting a local verdict",
        module="cratekit.cli.review", builder="build_import", handler_key="review.import",
        emits=frozenset({"review_set"}), output_schema="review_set/1",
    ),
    # ── Deferred routing (U19) ──────────────────────────────────────────────
    # Appended rather than beside its siblings, for the reason above. Every
    # later block is appended the same way.
    Entry(
        name="route.pending",
        summary="place tracks whose routing was decided before the library held a row for them",
        module="cratekit.write.routing_cli", builder="build_pending", handler_key="route.pending",
        feature_rows=(13,), emits=frozenset({"plan"}), output_schema="plan/1",
        writes=frozenset({"db_tree"}), destructive=True,
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(CLOUD_SYNC_UNREADABLE_GATE,),
    ),
    # ── Landing (U72) ───────────────────────────────────────────────────────
    Entry(
        name="intake.land",
        summary="move a folder of acquired files into the library and write one intake file",
        module="cratekit.intake.land_cli", builder="build_land", handler_key="intake.land",
        feature_rows=(3, 35), emits=frozenset({"plan"}), output_schema="plan/1",
        #: Files and one intake XML, never replacing a target, one lock per batch
        #: name (R-432). On a database native intake tree, content rows and a
        #: batch playlist behind the explicit gate (R-746). A set landing may
        #: archive the account playlist (U129); a landed heart is coloured (U153).
        writes=frozenset({"xml", "files", "db_tree", "db_metadata", "remote"}), destructive=True,
        #: The database checks hold for the native medium only;
        #: ``credential.provider`` is for the account archive (U129).
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
            "credential.provider",
        ),
        gates=(
            GateSpec(
                name="intake.land.confirm", options=("apply", "abort"),
                prompt="Move these files into the library and write the intake file?",
                digest_source="plan",
            ),
            # Content rows, answered by a separate recorded act (R34, R-746).
            GateSpec(
                name="intake.land.native", options=("apply", "abort"),
                prompt="Move these files into the library and add them to the collection?",
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The deferred mark (U82) ─────────────────────────────────────────────
    Entry(
        name="sync.mark",
        summary="record the account playlists a landed sync pass finished as taken",
        module="cratekit.sync.mark_cli", builder="build_mark", handler_key="sync.mark",
        feature_rows=(3, 25), source_scripts=("dj-sync",), emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: No write surface (U242): the account is only read, and each playlist
        #: is held as taken in the mark record, this product's own state.
        writes=frozenset(), doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="sync.mark.confirm", options=("apply", "abort"),
                prompt="Record these playlists as taken?",
                # Explicit (R34): a taken playlist is never offered again.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── The mark, undone (R-838) ────────────────────────────────────────────
    Entry(
        name="sync.unmark",
        summary="let go what a sync pass took, and put back any title its mark wrote",
        module="cratekit.sync.unmark_cli", builder="build_unmark", handler_key="sync.unmark",
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only: ``rename_playlist`` back to the recorded title;
        #: a taken entry is let go in the record (U242). Destructive: the
        #: retitle lands on a playlist the product did not make.
        writes=frozenset({"remote"}), destructive=True, doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="sync.unmark.confirm", options=("apply", "abort"),
                prompt="Put these playlist titles back on the streaming account?",
                # Explicit, as ``sync.mark``'s is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── The DOWNLOADED prefix, retired (U242) ───────────────────────────────
    Entry(
        name="sync.taken",
        summary=(
            "record every account playlist already taken, the prefixed and the "
            "marked, in Cratekit's own record"
        ),
        module="cratekit.sync.taken_cli", builder="build_taken", handler_key="sync.taken",
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: No write surface: only the mark record, this product's own state.
        writes=frozenset(), doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="sync.taken.confirm", options=("apply", "abort"),
                prompt="Record these playlists as taken in Cratekit's own record?",
                #: Explicit (R34): a taken playlist is never offered again.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="sync.strip",
        summary=(
            "take the retired DOWNLOADED prefix off every account playlist, "
            "each recorded as taken first"
        ),
        module="cratekit.sync.strip_cli", builder="build_strip", handler_key="sync.strip",
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only: ``rename_playlist``, recorded first under
        #: ``prefix-strip`` so ``sync unmark`` can undo it. Destructive, for
        #: ``sync.unmark``'s reason.
        writes=frozenset({"remote"}), destructive=True, doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="sync.strip.confirm", options=("apply", "abort"),
                prompt=(
                    "Take the DOWNLOADED prefix off these playlists on the streaming "
                    "account?"
                ),
                # Explicit, as ``sync.unmark``'s is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── The import proof (R-501) ────────────────────────────────────────────
    Entry(
        name="intake.imported",
        summary="prove an intake file imported, retire it, and settle its run",
        module="cratekit.intake.imported_cli", builder="build_imported",
        handler_key="intake.imported", feature_rows=(3, 35), emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The intake file is renamed out of the pending scan, so destructive
        #: (KTD24). No gate: nothing is lost and renaming back undoes it.
        writes=frozenset({"xml", "files"}), destructive=True, doctor_checks=("library.mounted",),
    ),
    # ── The export, without rekordbox's menus (R-745) ───────────────────────
    Entry(
        name="export.collection",
        summary="write a collection export from a copy of the database, with rekordbox closed",
        module="cratekit.cli.export_collection", builder="build", handler_key="export.collection",
        # No feature row: the source system never produced an export.
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        #: One new XML, never replaced, so not destructive; the database is read
        #: through a copy. Core, since the verbs reading the file are core.
        #: ``library.paths_resolved`` counts the unmapped rows (R-773).
        writes=frozenset({"xml"}),
        doctor_checks=("library.mounted", "rekordbox.closed", "library.paths_resolved"),
    ),
    # ── The folder suggestion (R-797) ───────────────────────────────────────
    Entry(
        name="report.genres",
        summary=(
            "name every genre holding 50 or more tracks with no top level "
            "folder of its own; creates nothing"
        ),
        module="cratekit.adopt.genres_cli", builder="build", handler_key="report.genres",
        # No feature row. The adoption module, not reports: it reads the
        # database through adoption's collection reader.
        module_id="adoption", emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # The database is only read, as for ``route.unplaced``; the pins stay.
        taxonomy_terms=("genre_energy",), doctor_checks=("library.mounted", "rekordbox.pins"),
    ),
    # ── A row's genre from its file (R-816) ─────────────────────────────────
    Entry(
        name="tag.rows",
        summary=(
            "write each library row's genre from its file where the two "
            "disagree, the genre and nothing else; writes no file"
        ),
        module="cratekit.tagging.rows_cli", builder="build", handler_key="tag.rows",
        # No feature row or source script. Gated by ``repair``, for
        # ``tag.retag``'s reason.
        module_id="repair", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The row only, the ``GenreID`` relink (R-246); the file is the authority.
        writes=frozenset({"db_metadata"}), destructive=True, taxonomy_terms=("genre_energy",),
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            # Unmapped rows are left alone, so the ratio decides the plan.
            "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="tag.rows.confirm", options=("apply", "abort"),
                prompt="Write the genre on these rows from their files?",
                #: Explicit (R34): a write to rows of a live library.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The genres an older mapping wrote, corrected on the file (R-799) ────
    Entry(
        name="tag.remap",
        summary=(
            "rewrite the genre on files a tag job filed by a mapping the "
            "taxonomy has since changed, from what the job recorded; writes no row"
        ),
        module="cratekit.tagging.remap_cli", builder="build", handler_key="tag.remap",
        # No feature row or source script. Gated by ``repair``, as ``tag.rows`` is.
        module_id="repair", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The file only: the row follows by ``tag.rows``, which the run names,
        #: so no database is opened and no cloud sync decision.
        writes=frozenset({"files"}), destructive=True, taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="tag.remap.confirm", options=("apply", "abort"),
                prompt="Rewrite the genre on these files?",
                #: Explicit (R34): a genre is written once and stays.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── A genre for a row with none (U114) ──────────────────────────────────
    Entry(
        name="tag.suggest",
        summary=(
            "suggest a genre for each row with none on the row or the file, "
            "from its artist, its folder and optionally the catalogues; writes file and row"
        ),
        module="cratekit.tagging.suggest_cli", builder="build", handler_key="tag.suggest",
        # No feature row or source script. Core, as ``tag.folder``: adoption
        # files by genre.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The file and the row, so they agree, the row as ``tag.rows`` writes it.
        writes=frozenset({"files", "db_metadata"}), destructive=True,
        taxonomy_terms=("genre_energy",),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="tag.suggest.confirm", options=("apply", "abort"),
                prompt="Write these suggested genres on the files and their rows?",
                #: Explicit (R34), for ``tag.rows.confirm``'s reason.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── A chosen genre over the one a row carries (U339) ────────────────────
    Entry(
        name="tag.set",
        summary=(
            "give the rows named a genre the taxonomy declares, over the one they "
            "carry, on the file and the row; writes file and row"
        ),
        module="cratekit.tagging.genre_set_cli", builder="build", handler_key="tag.set",
        # No feature row or source script. Core, as ``tag.suggest``: adoption
        # files by genre.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The file and the row, the row as ``tag.rows`` writes it; a genre with
        #: no lookup row writes nothing, since only a landing may make one.
        writes=frozenset({"files", "db_metadata"}), destructive=True,
        taxonomy_terms=("genre_energy",),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="tag.set.confirm", options=("apply", "abort"),
                prompt="Give these rows the genre, on their files and in rekordbox?",
                #: Explicit (R34), for ``tag.rows.confirm``'s reason.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── A second genre folder beside the genre's own (U340) ─────────────────
    Entry(
        name="tag.second",
        summary=(
            "set or clear a second genre on chosen rows' files, which files each "
            "track into that genre's folder too; writes no row"
        ),
        module="cratekit.tagging.second_cli", builder="build", handler_key="tag.second",
        # No feature row or source script. Core, as ``tag.suggest``: adoption
        # files by genre.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The file only: the database is read to find the rows, and the tree
        #: follows at the next filing, which the run names.
        writes=frozenset({"files"}), destructive=True, taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted", "rekordbox.pins", "library.paths_resolved"),
        gates=(
            GateSpec(
                name="tag.second.confirm", options=("apply", "abort"),
                prompt="Write this second genre on these files?",
                #: Explicit (R34): a genre is written once and stays.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── The needs genre backlog (U292) ──────────────────────────────────────
    Entry(
        name="tag.backlog",
        summary=(
            "sort every row adoption leaves under needs genre by cause, with "
            "each verb that settles it and one question per genre word no folder "
            "takes; writes nothing"
        ),
        module="cratekit.tagging.backlog_cli", builder="build", handler_key="tag.backlog",
        # No feature row or source script. Core, as ``tag.suggest``, whose plan
        # it reads; the diagnostic surface, as ``report.genres``.
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        # The database is only read; ``--catalogue`` answers are state, not a surface.
        taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted", "rekordbox.pins", "library.paths_resolved"),
    ),
    # ── The needs genre campaign (U294) ─────────────────────────────────────
    # A composer, as ``organize`` is: each step is another verb's, under one
    # gate over ``tag.backlog``'s plan.
    Entry(
        name="tag.campaign",
        summary=(
            "apply the needs genre backlog under one gate: tag rows, tag "
            "suggest at the floor, the answered words, then tag rows again; writes "
            "file and row, names the resort"
        ),
        module="cratekit.cli.verbs.tag_campaign", builder="build", handler_key="tag.campaign",
        # No feature row or source script. Gated by ``repair``, as ``tag.rows``,
        # its first and last step, so a composer is no way round a switch.
        module_id="repair", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The union of its steps' surfaces.
        writes=frozenset({"files", "db_metadata"}), destructive=True,
        taxonomy_terms=("genre_energy",),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="tag.campaign.approve", options=("apply", "abort"),
                prompt=(
                    "Apply the needs genre campaign: the rows from their files, "
                    "the suggestions at the floor, and the answered words, each through "
                    "its own verb? Filing them into their folders asks its own gate."
                ),
                #: Explicit (R34): it stands for its steps' explicit gates.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The INBOX rotation (U111) ───────────────────────────────────────────
    Entry(
        name="inbox.rotate",
        summary=(
            "move stale INBOX batches into INBOX / Old and remove expired ones "
            "from Old, never a track"
        ),
        module="cratekit.intake.rotate_cli", builder="build", handler_key="inbox.rotate",
        # The half of the source's rotation the aging report left to a person.
        feature_rows=(20,), source_scripts=("dj-inbox-rotation",), emits=frozenset({"plan"}),
        output_schema="plan/1",
        #: The tree only: intake playlist nodes moved or soft deleted.
        writes=frozenset({"db_tree"}), destructive=True, taxonomy_terms=("inbox", "inbox_old"),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="inbox.rotate.approve", options=("approve", "abort"),
                prompt=(
                    "Move these batches into Old and remove these from it, "
                    "keeping every track?"
                ),
                #: Explicit (R34): a removal takes a playlist out of the library.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The INBOX refill (U134) ─────────────────────────────────────────────
    # Rebuilds an emptied INBOX mirror of an account playlist.
    Entry(
        name="inbox.refill",
        summary=(
            "refill each INBOX playlist a pass mirrored from the author's account, "
            "every track the library owns in the account's order, memberships only"
        ),
        module="cratekit.intake.refill_cli", builder="build", handler_key="inbox.refill",
        # No feature row: the source never mirrored an account playlist.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: memberships of playlists under the intake root.
        writes=frozenset({"db_tree"}), taxonomy_terms=("inbox",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="inbox.refill.approve", options=("apply", "abort"),
                prompt="Add these tracks to their INBOX playlists?",
                #: Explicit (R34): a write outside the intake flow.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── INBOX / Analyze, cleared (U166) ─────────────────────────────────────
    # Clears the analysed rows out of the playlist the rekordbox visit selects.
    Entry(
        name="inbox.analyzed",
        summary=(
            "take every row rekordbox has analysed out of INBOX / Analyze, leaving "
            "each row still waiting, memberships only"
        ),
        module="cratekit.intake.analyzed_cli", builder="build", handler_key="inbox.analyzed",
        # No feature row: the source never kept an analysis queue.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: memberships of one intake playlist, soft deleted.
        writes=frozenset({"db_tree"}), taxonomy_terms=("inbox",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="inbox.analyzed.approve", options=("apply", "abort"),
                prompt=(
                    "Take these analysed tracks out of INBOX / Analyze, keeping "
                    "every track in the collection?"
                ),
                #: Explicit (R34): a removal from a playlist.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The rekordbox visit, checked (U167) ─────────────────────────────────
    # A read only verdict on the visit; its exit status lets a skill wait on it.
    Entry(
        name="analyze.check",
        summary=(
            "read rekordbox's analysis of the landed rows and say whether the visit "
            "is done, still waiting, or suspect; reads a copy, writes nothing"
        ),
        module="cratekit.analysis.check_cli", builder="build", handler_key="analyze.check",
        # No feature row. Core, not analysis: it runs no detector, and the
        # landing it follows is core.
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        doctor_checks=("library.mounted", "rekordbox.closed"),
    ),
    # ── After the visit, a title takes rekordbox's key and tempo (U327) ─────
    Entry(
        name="analyze.adopt",
        summary=(
            "after the rekordbox visit, give each landed title whose key or tempo "
            "differs rekordbox's, in the row's title, the file's title tag and its "
            "key tag; never a key column, a tempo field or a file name"
        ),
        module="cratekit.analysis.head_adopt_cli", builder="build",
        handler_key="analyze.adopt",
        # No feature row. Gated by the analysis module, which alone stamps a
        # head, with no extras: it runs no detector.
        module_id="analysis", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The title tag and key tag of each file, and the row's ``Title`` alone.
        writes=frozenset({"files", "db_metadata"}), destructive=True,
        doctor_checks=(
            "library.mounted",
            "rekordbox.closed",
            "rekordbox.pins",
            # A row whose file cannot be found is left, so the ratio decides the plan.
            "library.paths_resolved",
        ),
        gates=(
            GateSpec(
                name="analyze.adopt.confirm", options=("apply", "abort"),
                prompt="Give these titles rekordbox's key and tempo?",
                #: Explicit (R34): a write to files and rows of a live library.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The set's permanent playlist (U121) ─────────────────────────────────
    # The backfill for a set landed without ``--set``.
    Entry(
        name="intake.inspiration",
        summary=(
            "write a landed set's permanent playlist under INSPIRATION, every "
            "identified track the library owns in set order, named the source system's way"
        ),
        module="cratekit.intake.inspiration_cli", builder="build",
        handler_key="intake.inspiration",
        # No feature row: the source made these by hand.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: one playlist under INSPIRATION, and its memberships.
        writes=frozenset({"db_tree"}), taxonomy_terms=("inspiration",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="intake.inspiration.approve", options=("apply", "abort"),
                prompt="Write the set's playlist under INSPIRATION with these tracks?",
                #: Explicit (R34): the node stays in the library for good.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The genre Favorites (U119) ──────────────────────────────────────────
    # The one path that removes a genre Favorites membership.
    Entry(
        name="favorites.refresh",
        summary=(
            "make every genre folder's Favorites playlist mirror All Favorites, "
            "adding what the folder holds that is a favourite and removing what is not"
        ),
        module="cratekit.favorites.refresh_cli", builder="build", handler_key="favorites.refresh",
        # No feature row: the source kept no Favorites per genre.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: each genre's Favorites playlist and its memberships.
        writes=frozenset({"db_tree"}), destructive=True,
        taxonomy_terms=("genre_energy", "favorites"),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="favorites.refresh.approve", options=("approve", "abort"),
                prompt=(
                    "Make each genre folder's Favorites mirror All Favorites, adding "
                    "these and removing those?"
                ),
                #: Explicit (R34): a removal takes a membership away.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The landed hearts placed (U120) ─────────────────────────────────────
    # The backfill for hearts the landing did not place (U120, U146).
    Entry(
        name="favorites.backfill",
        summary=(
            "put every heart on the account whose track the library owns into All "
            "Favorites and the playlist of the month it was hearted in, adding and never removing"
        ),
        module="cratekit.favorites.backfill_cli", builder="build",
        handler_key="favorites.backfill",
        # No feature row: the landing does what the source's pass did.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: Memberships added, and the colour on members with none (U153).
        writes=frozenset({"db_tree", "db_metadata"}), destructive=True,
        taxonomy_terms=("favorites",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="favorites.backfill.approve", options=("approve", "abort"),
                prompt="Put these landed hearts into All Favorites and their month " "playlists?",
                #: Explicit (R34): a write to the live library's playlists.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The quarters split into months (U145) ───────────────────────────────
    # One time: splits the quarter playlists into months (U145).
    Entry(
        name="favorites.split",
        summary=(
            "split every quarter playlist beside All Favorites into the playlists of "
            "the months its hearts were hearted in, then retire the emptied quarters"
        ),
        module="cratekit.favorites.split_cli", builder="build", handler_key="favorites.split",
        # No feature row: the source filed by quarter.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: month memberships added, quarters soft deleted.
        writes=frozenset({"db_tree"}), destructive=True, taxonomy_terms=("favorites",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="favorites.split.approve", options=("approve", "abort"),
                prompt=(
                    "Put these quarter playlists' hearts into their month playlists and "
                    "retire the quarters?"
                ),
                #: Explicit (R34): it retires live playlists.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The Favorites folder put in order newest first (U180) ──────────────
    # One time: orders the months already in the folder newest first (U180).
    Entry(
        name="favorites.order",
        summary=(
            "put the folder that holds All Favorites in order: All Favorites first, "
            "the months newest first, then Undated, then everything else as it was"
        ),
        module="cratekit.favorites.order_cli", builder="build", handler_key="favorites.order",
        # No feature row: the source appended each month at the end.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: positions of the playlists in the Favorites folder.
        writes=frozenset({"db_tree"}), destructive=True, taxonomy_terms=("favorites",),
        doctor_checks=("library.mounted", "rekordbox.closed", "rekordbox.pins"),
        gates=(
            GateSpec(
                name="favorites.order.approve", options=("approve", "abort"),
                prompt="Put the Favorites folder in this order, newest month first?",
                #: Explicit (R34): it writes live playlist positions.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The retroactive tidy (U112) ─────────────────────────────────────────
    # A composer, as ``sync.all`` is: every step and write is another verb's.
    Entry(
        name="organize",
        summary=(
            "tidy rekordbox and the account by the product's own rules, one "
            "question per side; lists what you made and never moves it"
        ),
        module="cratekit.organize.cli", builder="build", handler_key="organize",
        # No feature row: each step's row is claimed by its own verb.
        emits=frozenset({"diagnostic"}), output_schema="diagnostic/1",
        #: The union of its steps' surfaces (U142, U144); no file is written.
        #: Destructive: the rotation, a mark and the root step (U143) remove or
        #: retitle what the product did not make.
        writes=frozenset({"db_tree", "db_metadata", "remote"}), destructive=True,
        taxonomy_terms=("genre_energy", "inbox", "inbox_old", "inspiration"),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "credential.provider",
        ),
        gates=(
            GateSpec(
                name="organize.rekordbox.approve", options=("approve", "abort"),
                prompt=(
                    "Apply these steps to the rekordbox library? Nothing you "
                    "made is moved and no track is removed."
                ),
                #: Explicit (R34): it stands for its steps' explicit gates.
                explicit=True, digest_source="plan",
            ),
            GateSpec(
                name="organize.account.apply", options=("apply", "abort"),
                prompt=(
                    "Apply these steps to the streaming account? Only the "
                    "removals listed are made: label debris whose tracks are in its "
                    "label's folder, empty root playlists, and an emptied legacy year "
                    "folder. A working custom playlist stays at the root until a "
                    "sync marks it downloaded, which files it in its year folder."
                ),
                #: Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── A label's dated playlist heard (U123) ───────────────────────────────
    # The half of U117 after the author has heard a go's releases.
    Entry(
        name="label.heard",
        summary=(
            "mark a label's dated playlist heard: its tracks go in the year "
            "playlist and the dated playlist is removed from the account"
        ),
        module="cratekit.label.heard_cli", builder="build_heard", handler_key="label.heard",
        feature_rows=(23,), module_id="labels", emits=frozenset({"plan"}), output_schema="plan/1",
        #: The account only; the Record Labels tree stays on the bridge (R39).
        #: Destructive: it removes a dated playlist this product created.
        writes=frozenset({"remote"}), destructive=True, doctor_checks=("credential.provider",),
        gates=(
            GateSpec(
                name="label.heard.confirm", options=("apply", "abort"),
                prompt=(
                    "Mark these releases heard, put the dated playlist's tracks in "
                    "the year, less any removed or pruned, and remove it from the "
                    "streaming account?"
                ),
                #: Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── The taxonomy copy brought up to the shipped schema (U132) ───────────
    # Brings what the shipped template gained into a library's copy.
    Entry(
        name="taxonomy.upgrade",
        summary=(
            "add the classes, buckets and vocabulary tables the shipped taxonomy "
            "template declares and this library's copy lacks, and state the shipped "
            "schema version"
        ),
        module="cratekit.cli.verbs.taxonomy", builder="build", handler_key="taxonomy.upgrade",
        # No feature row: the source's taxonomy was code.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: No declared surface: the taxonomy copy and its backup are library
        #: state. Not destructive: it only adds, keeping the old copy.
        writes=frozenset(),
        #: Not ``taxonomy.active``: the verb refuses an unusable copy itself.
        doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="taxonomy.upgrade.apply", options=("approve", "abort"),
                prompt=(
                    "Add these classes, buckets and vocabulary tables to this "
                    "library's taxonomy copy and state the shipped schema version?"
                ),
                #: Explicit (R34): every verb routes by the copy.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── A genre word outside the taxonomy, answered in one command (U194) ──
    # The two answers for a genre word the taxonomy has no place for.
    Entry(
        name="taxonomy.alias",
        summary=(
            "save a genre word the taxonomy has no place for as a tagging alias "
            "of one of its genre folders, and retag the files carrying it; writes files"
        ),
        module="cratekit.cli.verbs.taxonomy_word", builder="build_alias",
        handler_key="taxonomy.alias",
        # No feature row: the source's aliases were code.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The file only, beside the taxonomy copy (library state). Rows follow
        #: by ``tag.rows``, so no cloud sync decision. Destructive: a genre is replaced.
        writes=frozenset({"files"}), destructive=True, taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="taxonomy.alias.apply", options=("approve", "abort"),
                prompt=(
                    "Save this word as an alias of the genre in this library's "
                    "taxonomy copy, and retag the files carrying it?"
                ),
                #: Explicit (R34): every verb routes by the copy.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    Entry(
        name="taxonomy.folder",
        summary=(
            "make a genre word the taxonomy has no place for a genre folder of "
            "its own, with energy bands, in this library's taxonomy copy"
        ),
        module="cratekit.cli.verbs.taxonomy_word", builder="build_folder",
        handler_key="taxonomy.folder",
        # No feature row, for the alias's reason.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: No declared surface, as ``taxonomy.upgrade``; ``route.resort`` files
        #: the tracks after. Not destructive: it only adds.
        writes=frozenset(), doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="taxonomy.folder.apply", options=("approve", "abort"),
                prompt="Add this genre folder to this library's taxonomy copy?",
                #: Explicit (R34), as the upgrade's.
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── A playlist pair, kept one list on both sides (U130) ─────────────────
    Entry(
        name="sync.pair",
        summary=(
            "keep one of your account playlists and one rekordbox playlist the "
            "same list, each side merged against the last sync"
        ),
        module="cratekit.sync.pair_cli", builder="build", handler_key="sync.pair",
        # No feature row: the source kept no list on both sides.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The rekordbox playlist's memberships and the account playlist's
        #: tracks. Destructive: a membership is taken off on both sides.
        writes=frozenset({"db_tree", "remote"}), destructive=True,
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "credential.provider",
        ),
        gates=(
            GateSpec(
                name="sync.pair.rekordbox", options=("apply", "skip"),
                prompt=(
                    "Write these additions, removals and order to the rekordbox "
                    "playlists, and queue these tracks for acquisition?"
                ),
                #: Explicit, as every database membership write is (R34).
                explicit=True, digest_source="plan",
            ),
            GateSpec(
                name="sync.pair.account", options=("apply", "skip"),
                prompt=(
                    "Write these additions, removals and order to the streaming "
                    "account's playlists?"
                ),
                #: Explicit, as every account write is (R34).
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── The custom playlist twins' backfill (U149) ──────────────────────────
    Entry(
        name="sync.twins",
        summary=(
            "give every downloaded custom playlist on the account its permanent "
            "twin in rekordbox's Custom Playlists <year> folder, paired to stay one list"
        ),
        module="cratekit.sync.twins_cli", builder="build", handler_key="sync.twins",
        # No feature row: the source kept no rekordbox copy.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The tree only: year folders, twin playlists and memberships. Not
        #: destructive: it removes nothing.
        writes=frozenset({"db_tree"}),
        doctor_checks=(
            "library.mounted", "rekordbox.closed", "rekordbox.pins", "credential.provider",
        ),
        gates=(
            GateSpec(
                name="sync.twins.approve", options=("approve", "abort"),
                prompt=(
                    "Make these twins and their folders in rekordbox, and pair each "
                    "with its account playlist?"
                ),
                #: Explicit, as every database membership write is (R34).
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
    # ── A twin's held tracks, let go at the author's choice (U221) ──────────
    Entry(
        name="sync.release",
        summary=(
            "let a custom playlist twin's held tracks be queued at the next "
            "crate sync pair, one twin by its account playlist or every twin"
        ),
        module="cratekit.sync.release_cli", builder="build", handler_key="sync.release",
        # No feature row: the source queued every missing track unasked.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: No write surface: only the pairs document, this product's own state.
        writes=frozenset(), doctor_checks=("library.mounted",),
        gates=(
            GateSpec(
                name="sync.release.approve", options=("approve", "abort"),
                prompt=(
                    "Let these twins' held tracks be queued for download at the "
                    "next crate sync pair?"
                ),
                #: Explicit: it decides what is downloaded next (U221).
                explicit=True, digest_source="plan",
            ),
        ),
    ),
    # ── A genre for the files every catalogue missed (U172) ─────────────────
    Entry(
        name="tag.guess",
        summary=(
            "give each file in a folder with no genre one guessed from its "
            "artist's other tracks and the playlist it came from; writes files"
        ),
        module="cratekit.tagging.guess_cli", builder="build", handler_key="tag.guess",
        # No feature row or source script. Core, as ``tag.folder``: every pass
        # runs it.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The file only; the database is only read, so no cloud sync decision.
        #: No gate, as ``tag.folder``: every guess is written (U172).
        writes=frozenset({"files"}), destructive=True, taxonomy_terms=("genre_energy",),
        doctor_checks=("library.mounted",),
    ),
    # ── Tracks taken off a downloaded playlist (U287) ───────────────────────
    Entry(
        name="sync.removed",
        summary=(
            "list each downloaded track you took off its playlist on the streaming "
            "account, and take the offered ones out of the rekordbox collection behind a gate"
        ),
        module="cratekit.sync.removed_cli", builder="build_removed", handler_key="sync.removed",
        # No feature row. Core, as ``sync.taken``.
        emits=frozenset({"plan"}), output_schema="plan/1",
        #: The collection (U288): a row and everything naming it, deleted as
        #: Remove from Collection does, playlists renumbered (R-1830). No file:
        #: only ``delete review`` trashes one.
        writes=frozenset({"db_tree", "db_metadata"}), destructive=True,
        doctor_checks=(
            "credential.provider", "library.mounted", "rekordbox.closed", "rekordbox.pins",
        ),
        gates=(
            GateSpec(
                name="sync.removed.confirm", options=("apply", "abort"),
                prompt="Take these tracks out of the rekordbox collection?",
                #: Explicit (R34): a removal from the collection.
                explicit=True, digest_source="plan",
            ),
            GateSpec(
                name="sync.removed.retire", options=("retire", "abort"),
                prompt="Retire these playlists the account no longer has?",
                #: Explicit (U320): a retired playlist stops protecting its
                #: tracks from removal. Writes only Cratekit's own record.
                explicit=True, digest_source="plan",
            ),
            CLOUD_SYNC_UNREADABLE_GATE,
        ),
    ),
)
