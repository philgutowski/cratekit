"""Reserved cause pins for ``cli``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'cli/__init__.py': [
        'config-unusable',
        # 2026-11-06, R-1334: 'decision-required' left, the screen test moved to render.
        'decision-unknown-gate',
        'internal-error',
        # 2026-11-05, U206: the warning a run that looked an ISRC up carries.
        'isrc-lookups',
        'module-extras-missing',
        'provider-spend',
    ],
    'cli/converge.py': ['not-compared'],
    'cli/cutover.py': [
        'cutover-already-recorded',
        'cutover-root-unresolved',
        'cutover-tree-undeclared',
        'internal-error',
        'revert-nothing-recorded',
    ],
    # 2026-11-22, U303: doctor's checks moved into their family modules, each
    # literal with the check that reads it (U125, U132, U159, U185 joined them).
    # Measured on the merged tree; do not bring back a package-wide total tuple.
    'cli/doctor.py': ['doctor-check-failed', 'utf-8'],
    'cli/doctor_backup.py': ['rekordbox-backups'],
    'cli/doctor_library.py': ['internal-error', 'utf-8'],
    'cli/doctor_model.py': ['ls-remote'],
    'cli/doctor_state.py': [
        'commit-msg',
        'hook-impl',
        'merge-commit',
        'post-checkout',
        'post-commit',
        'post-merge',
        'post-rewrite',
        'pre-commit',
        'pre-merge-commit',
        'pre-push',
        'pre-rebase',
        'prepare-commit-msg',
    ],
    'cli/exit_codes.py': [
        'archive-holds-a-different-recording',
        'archive-verify-failed',
        'database-absent',
        'destination-not-configured',
        'encoder-failed',
        'encoder-missing',
        'fix-binary-override',
        'grant-path-access',
        'install-binary',
        'install-binary-source-unknown',
        'library-root-absent',
        'library-root-foreign',  # 2026-11-21, #893
        'library-root-unproven',  # 2026-11-21, #893
        'no-snapshot-available',
        'output-exists',
        'rclone-missing',
        'rekordbox-absence-unconfirmed',  # 2026-11-05, U211.
        'rekordbox-running',
        'remote-not-configured',
        'repair-backup-facts',
        'restore-not-confirmed',
        'restore-target-absent',
        'restore-transfer-failed',
        'snapshot-identity-unrecorded',
        'snapshot-library-mismatch',
        'snapshot-listing-failed',
        'snapshot-name-invalid',
        'source-missing',
        'source-unsupported',
        'unsupported-platform',
        'upgrade-cratekit',
    ],
    'cli/export_collection.py': [
        'export-location-not-a-file',
        'export-location-unmapped',
        'export-member-not-in-collection',
        'export-node-kind-unreadable',
        'export-node-unreachable',
        'export-rating-unreadable',
        'export-smart-playlist-omitted',
        'export-text-normalised',
        'library-export-unusable',
        'output-exists',
        'path-permission-denied',
    ],
    'cli/gates.py': [
        'blocked-by-pending-action',
        'decision-required',
        'decision-stale',
        'decision-unknown-gate',
        'gate-not-reached',  # 2026-11-06, R-1349: a decide on a gate its run has not reached.
        'gate-sibling-run',  # 2026-11-01, U186: the sibling run warning joined.
        'internal-error',
    ],
    'cli/handlers.py': ['config-drift', 'internal-error'],
    'cli/jobs.py': ['internal-error', 'job-unknown'],
    # 2026-11-10, U239: the landing a go's own run could not record.
    'cli/label_sync.py': [
        'intake-list-unusable',  # 2026-11-11, R-1499: a folder its tail cannot list.
        'label-sync-landing-unrecorded',
    ],
    # 2026-11-21, U298: the one config load and the gate lookup's refusal joined, home to every verb's.
    'cli/output.py': ['awaiting-human-action', 'config-unusable', 'internal-error'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'cli/rebuild.py': [
        'internal-error',
        'job-unknown',
        'no-derivable-tree',  # 2026-11-05, U219
        'no-native-tree',
        'rebuild-actor-required',
        'rebuild-tree-not-native',
        'tree-not-derived',  # 2026-11-05, U219
    ],
    'cli/registry.py': [
        'dj-analyze-validate',
        'dj-audit-genres',
        'dj-energy-calibrate',
        'dj-favorites',
        'dj-inbox-rotation',
        'dj-label',
        'dj-label-batch',
        'dj-label-library',
        'dj-pad-camelot',
        'dj-path-repair',
        'dj-pipeline',
        'dj-resort-energy',
        'dj-resort-genre',
        'dj-scan-playlists',
        'dj-set-builder',
        'dj-setid',
        'dj-sort-inbox',
        'dj-sort-unplaced',
        'dj-sync',
        'dj-tag-folder',
        'dj-tidal-login',
        'dj-vocal-calibrate',
        'dj-vocal-mytags',
        'dj-vocal-restamp',
        'dj-vox-backfill',
    ],
    'cli/render.py': [
        # 2026-11-06, R-1334: a gate's screen, an open gate's or a stale answer's.
        'decision-required',
        'decision-stale',
        'not-imported',
        'not-judged',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'cli/reports.py': ['report-as-of-invalid'],
    'cli/review.py': [
        'review-file-unusable',
        'review-selection-invalid',
        'review-verdict-conflict',
        'utf-8',
    ],
    # 2026-11-21, U295: the night pass's schedule joined.
    'cli/schedule.py': [
        'refused-by-policy',  # 2026-11-21, U295 review round one: root is refused.
        'schedule-agent-unusable',
        'schedule-agent-unwritten',
        'schedule-crate-unresolved',
        'schedule-launchctl-failed',
        'schedule-platform-unsupported',
    ],
    'cli/setup.py': [
        'config-unusable',
        'library-database-not-rekordbox',
        'library-root-unreachable',
        'library-volume-unmounted',
        'utf-8',
    ],
    # 2026-10-28, U152: the sync pass driver joined, with two new literals, its
    # download refusal and left open intake warning codes. 2026-11-01, U190: the
    # tail and the landing moved to ``cli/tail.py``, and their five with them.
    'cli/sync_land.py': [
        'intake-list-unusable',  # 2026-11-11, R-1499: a staging folder it cannot list.
        'job-driver-held',
        'job-unknown',  # 2026-11-01, U183: a --pass-run that names no pass.
        'outbound-export-required',
        'refused-by-policy',  # 2026-11-11, R-1499: a pass beside another download.
        'sync-land-download-refused',
        'sync-land-intake-left-open',
        'sync-land-tail-unrecorded',  # 2026-11-11, R-1499: a tail record not kept.
        'sync-land-without-vocals',  # 2026-11-01, U181
        'vocal-model',  # 2026-11-01, U181
        'vocal-scoring-unavailable',  # 2026-11-01, U181
    ],
    # 2026-11-01, U179: the Bandcamp source of the same driver, its fetch verb's
    # words and the closing report's three warnings.
    'cli/sync_bandcamp.py': [
        'bandcamp-fetch',
        'sync-bandcamp-fetch-refused',
        'sync-bandcamp-no-genre',
        'sync-bandcamp-tags-unread',
    ],
    # 2026-11-01, U190: the tail and the landing, lifted out of the sync pass
    # driver so ``label sync --go`` runs the same chain.
    # 2026-11-21, U293: the night pass joined.
    'cli/sync_night.py': [
        'intake-list-unusable',
        'internal-error',
        'job-driver-held',
        'nothing-new',
        'refused-by-policy',
        'sync-night-status-unwritten',
        'utf-8',
        'waiting-at-acknowledgment',
        'waiting-at-gate',
    ],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'cli/tail.py': [
        'backup-acknowledgment-missing',
        'decision-required',
        'internal-error',
        # 2026-11-05, U212: the name step's refusal it reads for a second copy.
        'rename-incomplete',
        'source-missing',
    ],
    'cli/verbs/login.py': ['credential-missing', 'utf-8'],
    # 2026-10-31, U168: run decide --continue names the answer it continued on.
    'cli/verbs/runs.py': ['decision-recorded', 'decision-unknown-gate', 'run-not-continuable'],
    # Re-pinned on the merge of main at e686759 (U125) into fable/300, 2026-10-10:
    # a new module, crate taxonomy upgrade (U132). Its three WARNING codes are
    # the literals new to the package; the rest were already declared.
    # Measured on the merged tree; do not bring back a package-wide total tuple.
    # 2026-10-12, U133: the keyword rule warning joined.
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'cli/verbs/taxonomy.py': [
        'internal-error',
        'taxonomy-nothing-to-upgrade',
        'taxonomy-upgrade-held',
        'taxonomy-upgrade-keyword-rule',
        'taxonomy-upgraded',
        'utf-8',
    ],
    # 2026-11-21, U294: a new module, crate tag campaign. Its notes, the
    # states of its steps, and its three causes.
    'cli/verbs/tag_campaign.py': [
        'campaign-landed',
        'campaign-moved-since-plan',
        'campaign-nothing-to-write',
        'campaign-remainder',
        'campaign-resort-next',
        'campaign-rows-left',
        'campaign-words-left',
        'config-unusable',
        'file-carries-another-spelling',
        'internal-error',
        'not-run',
        'nothing-to-write',
        'review-selection-invalid',
        'tag-campaign',
    ],
    # 2026-11-02, U194: a new module, crate taxonomy alias and crate taxonomy
    # folder. Its notes, its three causes and the kind of a left file.
    'cli/verbs/taxonomy_word.py': [
        'config-unusable',
        'several-genres',
        'source-missing',
        'taxonomy-alias-file-not-read',
        'taxonomy-alias-left-alone',
        'taxonomy-alias-nothing-to-do',
        'taxonomy-alias-retagged',
        'taxonomy-alias-saved',
        'taxonomy-folder-already-declared',
        'taxonomy-folder-made',
        'taxonomy-genre-unknown',
        'taxonomy-word-refused',
        'taxonomy-word-unwritten',
    ],
}

NAMED_WITHOUT_OWN = {
    # 2026-10-28, U152: the sync pass driver's two stops and the unasked write.
    # 2026-11-01, U190: the two stops moved to ``cli/tail.py`` with the landing.
    'cli/sync_land.py': [
        'outbound-export-required',
        'vocal-scoring-unavailable',  # 2026-11-01, U181
    ],
    # 2026-11-01, U190: the landing's two stops, lifted out of the sync pass driver.
    'cli/tail.py': [
        'backup-acknowledgment-missing',
        'decision-required',
        'rename-incomplete',  # 2026-11-05, U212: read for a second copy.
    ],
}

NAMED_WITH_OWN = {
    # 2026-10-28, U152: the sync pass driver's two stops and the unasked write.
    # 2026-11-01, U190: the two stops moved to ``cli/tail.py`` with the landing.
    'cli/sync_land.py': [
        'outbound-export-required',
        'vocal-scoring-unavailable',  # 2026-11-01, U181
    ],
    # 2026-11-01, U190: the landing's two stops, lifted out of the sync pass driver.
    'cli/tail.py': [
        'backup-acknowledgment-missing',
        'decision-required',
        'rename-incomplete',  # 2026-11-05, U212: read for a second copy.
    ],
}

LITERAL_HOLDERS = {
    'cli/label_sync.py': ['intake-list-unusable'],  # 2026-11-11, R-1499 round one.
    # 2026-10-28, U152: the sync pass driver joined. 2026-11-01, U190: five
    # moved to ``cli/tail.py`` with the tail and the landing.
    'cli/sync_land.py': [
        'intake-list-unusable',  # 2026-11-11, R-1499: a staging folder it cannot list.
        'job-driver-held',
        'job-unknown',  # 2026-11-01, U183: a --pass-run that names no pass.
        'outbound-export-required',
        'refused-by-policy',  # 2026-11-11, R-1499: a pass beside another download.
        'vocal-scoring-unavailable',  # 2026-11-01, U181
    ],
    # 2026-11-01, U190: the tail and the landing, lifted out of the sync pass driver.
    # 2026-11-21, U293: the night pass joined.
    'cli/sync_night.py': ['intake-list-unusable', 'internal-error', 'job-driver-held', 'refused-by-policy'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'cli/tail.py': [
        'backup-acknowledgment-missing',
        'decision-required',
        'internal-error',
        'rename-incomplete',  # 2026-11-05, U212: read for a second copy.
        'source-missing',
    ],
    'cli/__init__.py': [
        'config-unusable',
        # 2026-11-06, R-1334: 'decision-required' left, the screen test moved to render.
        'decision-unknown-gate',
        'internal-error',
        'module-extras-missing',
    ],
    'cli/cutover.py': [
        'cutover-already-recorded',
        'cutover-root-unresolved',
        'cutover-tree-undeclared',
        'internal-error',
    ],
    # 2026-11-22, U303: internal-error moved with the taxonomy.schema check (U132).
    'cli/doctor.py': ['doctor-check-failed'],
    'cli/doctor_library.py': ['internal-error'],
    'cli/export_collection.py': ['library-export-unusable', 'output-exists', 'path-permission-denied'],
    'cli/gates.py': [
        'blocked-by-pending-action',
        'decision-required',
        'decision-stale',
        'decision-unknown-gate',
        'gate-not-reached',  # 2026-11-06, R-1349
        'internal-error',
    ],
    'cli/handlers.py': ['internal-error'],
    'cli/jobs.py': ['internal-error', 'job-unknown'],
    # 2026-11-21, U298: the one config load and the gate lookup's refusal joined, home to every verb's.
    'cli/output.py': ['awaiting-human-action', 'config-unusable', 'internal-error'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'cli/rebuild.py': [
        'internal-error',
        'job-unknown',
        'rebuild-actor-required',
        'rebuild-tree-not-native',
    ],
    # 2026-11-01, U182: the stale cancel's list says which jobs it cancelled.
    # 2026-11-06, R-1334: a gate's screen, an open gate's or a stale answer's.
    'cli/render.py': ['cancelled', 'decision-required', 'decision-stale'],
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'cli/reports.py': ['report-as-of-invalid'],
    'cli/review.py': ['review-file-unusable', 'review-selection-invalid'],
    # 2026-11-21, U295: the night pass's schedule joined.
    'cli/schedule.py': [
        'refused-by-policy',  # 2026-11-21, U295 review round one: root is refused.
        'schedule-agent-unusable',
        'schedule-agent-unwritten',
        'schedule-crate-unresolved',
        'schedule-launchctl-failed',
        'schedule-platform-unsupported',
    ],
    'cli/setup.py': [
        'config-unusable',
        'library-database-not-rekordbox',
        'library-root-unreachable',
        'library-volume-unmounted',
    ],
    'cli/verbs/login.py': ['credential-missing'],
    # 2026-10-31, U168: a run with no command line to continue is refused.
    'cli/verbs/runs.py': ['decision-unknown-gate', 'run-not-continuable'],
    # 2026-11-21, U294: a new module, crate tag campaign.
    'cli/verbs/tag_campaign.py': ['config-unusable', 'internal-error', 'review-selection-invalid'],
    # Re-pinned on the merge of main at e686759 (U125) into fable/300, 2026-10-10:
    # a new module, crate taxonomy upgrade (U132). Measured on the merged tree.
    # 2026-11-21, U298: the literal left with the helper it named, which has one home now.
    'cli/verbs/taxonomy.py': ['internal-error'],
    # 2026-11-02, U194: a new module, crate taxonomy alias and folder.
    'cli/verbs/taxonomy_word.py': [
        'config-unusable',
        'source-missing',
        'taxonomy-genre-unknown',
        'taxonomy-word-refused',
        'taxonomy-word-unwritten',
    ],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'cli/doctor.py',
    'cli/gates.py',  # 2026-11-01, U186: the sibling window's twelve hours.
    'cli/schedule.py',  # 2026-11-21, U295: launchctl's not found code and its timeout.
    'cli/output.py',
})
