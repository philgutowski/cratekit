"""Reserved cause pins for ``core``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'core/active_taxonomy.py': ['config-unusable', 'library-volume-unmounted', 'utf-8'],
    'core/backup_facts.py': [
        'grant-path-access',
        'never-recorded',
        'recorded-in-the-future',
        'repair-backup-facts',
        'upgrade-cratekit',
        'utf-8',
    ],
    'core/binaries.py': [
        'fix-binary-override',
        'from-source',
        'install-binary',
        'install-binary-source-unknown',
        'keyfinder-cli',
        'unsupported-platform',
        'yt-dlp',
    ],
    'core/binary_refusal.py': ['yt-dlp-missing'],
    'core/cause.py': [
        'account-mirror-ambiguous',  # 2026-10-15, U147
        'adapter-broken',
        'adopt-entries-failed',
        'adopt-item-absent',
        'adoption-file-unidentifiable',
        'adoption-ledger-unusable',
        'analysis-check-landing-unknown',  # 2026-10-31, U167
        'analysis-suspect',  # 2026-10-31, U167
        'analysis-write-failed',
        'analyze-adopt-unwritten',  # 2026-11-23, U327
        'anlz-modified',
        'app-version-pin-drift',
        'app-version-pin-unrecorded',
        'archive-holds-a-different-recording',
        'archive-verify-failed',
        'auth-failed',
        'awaiting-human-action',
        'awaiting-import',
        # 2026-10-12, U138: the session's age rule refusal joined.
        'backup-acknowledgment-backup-too-old',
        'backup-acknowledgment-missing',
        'backup-acknowledgment-no-terminal',
        'backup-facts-unreadable',
        'backup-nothing-ran',
        'backup-transfer-failed',
        'bandcamp-label-unwritten',  # 2026-11-01, U177
        'bandcamp-record-unusable',  # 2026-10-28, U176
        'blocked-by-pending-action',
        'canary-read-failed',
        'catalog-tree-undeclared',
        'catalogue-parse-broken',
        'catalogue-unreachable',
        'cloud-sync-active',
        'cloud-sync-unreadable',
        'collection-row-unmapped',
        'collection-unreadable',
        'config-unusable',
        'credential-index-unreadable',
        'credential-missing',
        'cutover-already-recorded',
        'cutover-export-missing',
        'cutover-native-write-taken',
        'cutover-open-run',
        'cutover-root-unresolved',
        'cutover-snapshot-missing',
        'cutover-tree-undeclared',
        'cutover-xml-pending',
        'database-absent',
        'database-open-failed',
        'db-schema-pin-drift',
        'decision-required',
        'decision-stale',
        'decision-unknown-gate',
        'deletion-evidence-incomplete',
        'deletion-reference-set-incomplete',
        'deletion-watermark-unusable',
        'destination-not-configured',
        'doctor-check-failed',
        'encoder-failed',
        'encoder-missing',
        'energy-calibration-missing',
        'energy-calibration-unreadable',
        'export-playlist-ambiguous',
        'export-playlist-empty',
        'export-playlist-unknown',
        'export-set-ambiguous',
        # 2026-10-13, U140: the set rename's refusal joined.
        'export-set-rename-unresolved',
        'favorites-class-undeclared',
        'favorites-pink-colour-missing',
        'favorites-source-missing',
        'gate-not-reached',  # 2026-11-06, R-1349
        'governed-tree-absent',
        'inspiration-folder-undeclared',
        'intake-export-is-stub',
        'intake-flow-absent',
        'intake-list-unusable',
        'intake-old-undeclared',
        'intake-recognition-failed',
        'intake-recognition-spend-bound',
        'intake-recognition-unready',
        'intake-staging-refused',
        'internal-error',
        'job-driver-held',
        'job-not-retryable',
        'job-schema-mismatch',
        'job-unknown',
        'label-catalogue-unbound',
        'label-heard-ambiguous',
        'label-heard-invalid',
        'label-heard-no-releases',
        'label-heard-no-year-playlist',
        'label-heard-not-in-playlist',
        'label-heard-not-product-made',
        'label-intent-unusable',
        'label-list-unusable',
        'label-listing-kept-unusable',  # 2026-11-05, U217.
        'label-name-invalid',
        'label-new-playlists-no-folder',
        'label-playlist-unreadable',
        'label-playlists-ambiguous',
        'label-playlists-incomplete',
        'label-playlists-reads-unusable',  # 2026-11-01, R-1091.
        'label-registry-empty',
        'label-sweep-incomplete',
        'label-sync-unanswerable',
        'label-sync-unlisted',  # R-1114, 2026-11-01
        'label-sync-unusable',
        'label-unknown',
        'label-watermark-unusable',
        'library-database-missing',
        'library-database-not-rekordbox',
        'library-directory-missing',
        'library-export-unusable',
        'library-fingerprint-unreadable',
        'library-paths-majority-unresolved',
        'library-root-absent',
        'library-root-foreign',  # 2026-11-21, #893
        'library-root-unproven',  # 2026-11-21, #893
        'library-root-unreachable',
        'library-volume-mismatch',
        'library-volume-unmounted',
        'link-majority-unclear',
        'link-probe-invalid',
        'link-row-unknown',
        'link-value-minority',
        'link-value-unheld',
        'lossy-refused',
        'mapped-volume-mismatch',
        'mapped-volume-unmounted',
        'mixed-permanent-failures',
        'module-extras-missing',
        'mytag-category-template-missing',
        'no-evidence',
        'no-snapshot-available',
        'outbound-account-unbound',
        'outbound-export-required',
        'outbound-item-absent',
        'outbound-ledger-unusable',
        'outbound-record-moved',
        'outbound-remove-refused',
        'output-exists',
        'path-locked',
        'path-permission-denied',
        'path-read-only',
        'provider-blocked',
        'provider-budget',  # 2026-11-12, U278
         'provider-call-ceiling',  # 2026-11-02, U193
        'provider-cooldown',
        'provider-gate-held',
        'provider-night-budget',  # 2026-11-21, U293
        'pyrekordbox-pin-drift',
        'rating-scale-unknown',
        'rclone-missing',
        'read-only',
        'rebuild-actor-required',
        'rebuild-derivation-empty',
        'rebuild-derivation-incomplete',
        'rebuild-tree-not-derivable',  # 2026-11-05, U219
        'rebuild-tree-not-native',
        'recovery-target-refused',
        'refill-playlist-outside-inbox',
        'refused-by-policy',
        'rekordbox-absence-unconfirmed',  # 2026-11-05, U211.
        'rekordbox-running',
        'remote-not-configured',
        'removal-sequence-unreadable',
        'rename-incomplete',
        'report-as-of-invalid',
        'resort-plan-stale',  # 2026-11-05, U219
        'restore-discards-committed-work',
        'restore-flag-needs-pull',
        'restore-not-confirmed',
        'restore-reconciliation-outstanding',
        'restore-record-unusable',
        'restore-staging-occupied',
        'restore-step-failed',
        'restore-tags-unwritten',  # 2026-11-23, R-1924
        'restore-target-absent',
        'restore-target-invalid',
        'restore-target-is-live-root',
        'restore-transfer-failed',
        'review-already-resolved',
        'review-file-unusable',
        'review-item-unknown',
        'review-option-unknown',
        'review-queue-undeclared',
        'review-schema-mismatch',
        'review-selection-invalid',
        'root-folder-missing',  # 2026-11-01, U169
        'routing-destination-renamed',
        'routing-ledger-unusable',
        'routing-outstanding',
        'run-not-continuable',  # 2026-10-31, U168
        'schedule-agent-unusable',  # 2026-11-21, U295
        'schedule-agent-unwritten',  # 2026-11-21, U295
        'schedule-crate-unresolved',  # 2026-11-21, U295
        'schedule-launchctl-failed',  # 2026-11-21, U295
        'schedule-platform-unsupported',  # 2026-11-21, U295
        'session-committed-unverified',
        'session-lock-held',
        'set-playlist-unnamed',
        'setbuild-anchor-ambiguous',
        'setbuild-anchor-not-indexed',
        'setbuild-anchor-outside-library',
        'setbuild-anchor-unknown',
        'setbuild-supplied-needs-unowned',
        'setbuild-unowned-key-missing',
        'smoke-test-failed',
        'snapshot-check-temp-full',  # 2026-11-13, R-1677: the check's throwaway copy with no room.
        'snapshot-identity-unrecorded',
        'snapshot-integrity-failed',
        'snapshot-library-mismatch',
        'snapshot-listing-failed',
        'snapshot-name-invalid',
        'snapshot-store-full',
        'soft-delete-marker-unreadable',
        'source-missing',
        'source-unsupported',
        'staging-held',  # 2026-11-21, U293
        'sync-artifacts-unusable',
        'sync-mark-record-unusable',
        'sync-marks-blocked',
        # 2026-10-10, U130: the four sync pair causes joined.
        'sync-pair-account-lagging',  # 2026-11-06, U226.
        'sync-pair-account-settling',  # 2026-11-06, U231.
        'sync-pair-conflict',
        'sync-pair-out-of-scope',
        'sync-pair-steps-unwritten',  # 2026-11-05, U210.
        'sync-pair-store-unusable',
        'sync-pair-unknown',
        'sync-release-not-a-twin',  # 2026-11-05, U221.
        'sync-release-unnamed',  # 2026-11-05, U221.
        'sync-source-lookups-failed',
        'sync-unavailable-record-unusable',  # 2026-11-21, U320.
        'sync-watermark-unusable',
        'tag-folder-unwritten',
        'tag-remap-unwritten',
        'tag-retag-folder-unknown',
        'tag-retag-unwritten',  # 2026-11-01, R-1103
        'tag-suggest-unwritten',
        'target-lufs-out-of-range',
        'taxonomy-genre-unknown',  # 2026-11-02, U194
        'taxonomy-word-refused',
        'taxonomy-word-unwritten',
        'trash-unavailable',
        'tree-convergence-unusable',
        'tree-registry-unusable',
        'tree-unconverged',
        'unavailable-permanent',
        'unavailable-transient',
        'verb-retired',
        'vocal-calibration-unreadable',
        'vocal-cut-out-of-range',
        'vocal-scoring-unavailable',  # 2026-11-01, U181
        'whitelist-violation',
        'write-lock-held',
        'yt-dlp-missing',
    ],
    # 2026-11-22, U299: the state inventory moved to its own module.
    'core/config.py': [
        'fix-config-values',
        'record-rekordbox-pin',
        'repair-config-file',
        'retry-when-unlocked',
        'run-setup',
        'upgrade-cratekit',
        'utf-8',
    ],
    'core/config_schema.py': ['utf-8'],  # 2026-11-22, U299
    'core/convergence.py': [
        'library-fingerprint-unreadable',
        'rows-moved-at-a-standstill',
        'sequence-went-backward',
        'tree-convergence-unusable',
        'tree-rebuild',
        'tree-unconverged',
        'utf-8',
    ],
    'core/discovery.py': ['folder-unreadable', 'internal-error', 'linked-folder-skipped'],
    'core/exit_codes.py': [
        'acknowledge-backup',
        'answer-decision',
        'authenticate-provider',
        'change-policy-or-input',
        'choose-known-adapter',
        'complete-pending-action',
        'disable-cloud-sync',
        'fix-binary-override',
        'fix-command-line',
        'fix-config-values',
        'grant-path-access',
        'install-adapter',
        'install-binary',
        'install-binary-source-unknown',
        'install-keychain-backend',
        'install-module-extra',
        'mount-library-volume',
        'pause-and-check-account',
        'prepare-library-in-rekordbox',
        'quit-rekordbox',
        'reauthenticate-provider',
        'rebuild-tree',
        'record-rekordbox-pin',
        'relax-lossless-policy',
        'release-stale-lock',
        'remount-writable',
        'repair-adapter-settings',
        'repair-backup-facts',
        'repair-config-file',
        'repair-credential-store',
        'replan-then-decide',
        'report-defect',
        'restore-from-snapshot',
        'resume-job',
        'retry-later',
        'retry-when-unlocked',
        'revalidate-pins',
        # 2026-10-12, U138: the remedy a too old backup refusal carries joined.
        'run-backup',
        'run-doctor',
        'run-setup',
        'set-credential',
        'switch-adapter',
        'unlock-path',
        'unsupported-platform',
        'upgrade-cratekit',
        'wait-for-holder',
    ],
    # 2026-11-22, U301: the drive loop moved to core/jobs_drive.py.
    'core/jobs.py': [
        'internal-error',
        'job-driver-held',
        'job-not-retryable',
        'job-schema-mismatch',
        'job-unknown',
        'no-evidence',
        'utf-8',
    ],
    'core/jobs_drive.py': ['internal-error', 'mixed-permanent-failures', 'unavailable-transient'],
    'core/naming.py': ['utf-8'],
    # 2026-11-11, U241: the name of the thread a stream worker watches its parent with.
    # 2026-11-21, U293: the night's ledger joined.
    'core/night_budget.py': ['utf-8'],
    'core/pool.py': ['cratekit-pool-parent-watch'],
    'core/preflight.py': ['if-root-can-be-created', 'if-root-exists'],
    # 2026-11-05, U211: the scan's refusal for a process it could not read.
    'core/processes.py': ['rekordbox-absence-unconfirmed'],
    # 2026-11-02, U193: the call ceiling's stop joined.
    # 2026-11-21, U293: the night pass's line joined.
    'core/provider_gate.py': ['provider-budget', 'provider-call-ceiling', 'provider-cooldown', 'provider-gate-held', 'provider-night-budget', 'utf-8'],  # 2026-11-12, U278
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/rb_copies.py': ['canary-read-failed'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/rb_nodes.py': ['mytag-category-template-missing', 'utf-8', 'whitelist-violation'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/rb_removal.py': ['soft-delete-marker-unreadable', 'utf-8', 'whitelist-violation'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/rb_tables.py': ['row-defaults', 'row-file-id', 'row-probe', 'track-color'],
    # 2026-11-12, U267: the shared read's refusal of a use it was not made for.
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/rb_writer.py': [
        'app-version-pin-drift',
        'app-version-pin-unrecorded',
        'canary-read-failed',
        'cloud-sync-active',
        'cloud-sync-unreadable',
        'database-open-failed',
        'db-schema-pin-drift',
        'internal-error',
        'library-database-missing',
        'library-database-not-rekordbox',
        'library-directory-missing',
        'mytag-category-template-missing',
        'pyrekordbox-pin-drift',
        'rekordbox-running',
        'soft-delete-marker-unreadable',
        'whitelist-violation',
        'write-lock-held',
    ],
    'core/reconcile.py': [
        'in-flight-restore',
        'restore-reconciliation-outstanding',
        'restore-record-unusable',
        'unconverged-tree',
        'utf-8',
    ],
    # 2026-10-31, U162: the rehearsal area helper joined.
    'core/rehearsal.py': ['internal-error', 'output-exists'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/restore.py': [
        'bare-metal-recovery',
        'capture-restore',
        'clear-companion',
        'internal-error',
        'library-session',
        'mark-trees-unconverged',
        'record-reconciliation',
        'rekordbox-running',
        'release-restore-latch',
        'remove-absent',
        'replace-directory',
        'replace-file',
        'resolve-session',
        'restore-discards-committed-work',
        'restore-step-failed',
        'snapshot-integrity-failed',
    ],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/restore_perform.py': [
        'internal-error',
        'restore-predates-cutover',
        'restore-staging-occupied',
        'restore-step-failed',
    ],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/restore_recovery.py': ['recovery-target-refused'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/restore_retention.py': ['internal-error'],
    # 2026-11-23, R-1924: a restore refusing a record it cannot put the files back from.
    'core/restore_tags.py': ['restore-record-unusable'],
    # 2026-11-22, U301: the exchange and the grouping moved to modules of their own.
    'core/review.py': [
        'awaiting-human-action',
        'fallback-source',
        'label-release',
        'path-repair',
        'review-already-resolved',
        'review-file-unusable',
        'review-item-unknown',
        'review-option-unknown',
        'review-queue-undeclared',
        'review-schema-mismatch',
        'review-selection-invalid',
        'utf-8',
        'version-match',
    ],
    'core/review_exchange.py': [
        'item-unusable',
        'local-verdict-stands',
        'review-file-unusable',
        'verdict-not-applied',
        'verdict-unreadable',
    ],
    'core/review_groups.py': ['label-release', 'review-selection-invalid'],
    'core/routing.py': ['not-judged'],
    'core/secrets.py': [
        'bandcamp-session',  # 2026-10-28, U176
        'catalogue-app-id',  # 2026-11-05, U205
        'catalogue-app-key',  # 2026-11-05, U205
        'credential-index-unreadable',
        'cyanite-key',  # 2026-11-13, U245
        'discogs-token',  # 2026-11-12, U244
        'identify-key',
        'identify-signing-key',
        'install-keychain-backend',
        'provider-session',
        'repair-credential-store',
        'set-credential',
        'utf-8',
    ],
    # 2026-10-12, U138: the session's age rule refusal and its rule name joined.
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/session.py': [
        'awaiting-import',
        'committed-unverified',
        'internal-error',
        'session-committed-unverified',
        'utf-8',
    ],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/session_ack.py': [
        'backup-acknowledgment-backup-too-old',
        'backup-acknowledgment-missing',
        'backup-acknowledgment-no-terminal',
        'backup-facts-unreadable',
        'internal-error',
        'session-ages',
        'utf-8',
    ],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/session_analysis.py': ['anlz-modified'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/session_holders.py': ['internal-error', 'session-lock-held'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/session_volumes.py': [
        'library-volume-mismatch',
        'library-volume-unmounted',
        'mapped-volume-mismatch',
        'mapped-volume-unmounted',
    ],
    # 2026-11-13, R-1677: the check's throwaway copy with no room joined.
    'core/snapshot.py': [
        'internal-error',
        'library-database-missing',
        'snapshot-check-temp-full',
        'snapshot-integrity-failed',
        'snapshot-store-full',
        'utf-8',
    ],
    # 2026-11-21, U293: the staging lock joined.
    'core/staging_lock.py': ['staging-held'],
    'core/tags.py': ['utf-8'],
    # 2026-11-22, U299: the state inventory, moved from core/config.py.
    'core/state_files.py': [
        'downloaded-file',
        'never-restored',
        'remote-playlist-prefix',
        'runs-held',  # 2026-11-05, U209: the held plans' state directory.
        'survives-rollback',
        'trashed-file',
        'written-file-tag',
    ],
    'core/taxonomy.py': ['utf-8'],
    # Re-pinned on the merge of main at e686759 (U125) into fable/300, 2026-10-10:
    # a new module, the taxonomy upgrade planner (U132), holding two causes
    # already declared. Measured on the merged tree.
    'core/taxonomy_upgrade.py': ['config-unusable', 'internal-error'],
    # 2026-11-02, U194: a new module, the off taxonomy word's planner. Its
    # kinds of refusal, read by the verb and carried in a refusal's detail.
    # 2026-11-02, R-1184: 'own-name' joined, a genre folder's own name in
    # another case.
    'core/taxonomy_word.py': [
        'already-filed',
        'bare-folder',
        'no-such-genre',
        'no-word',
        'not-editable',
        'own-name',
        'too-coarse',
        'would-not-load',
    ],
    'core/tombstone.py': ['removed-file', 'review-selection-invalid', 'version-uncredited'],
    'core/tree_registry.py': [
        'catalogue-crawl',
        'cutover-already-recorded',
        'cutover-export-missing',
        'cutover-native-write-taken',
        'cutover-open-run',
        'cutover-snapshot-missing',
        'cutover-xml-pending',
        'fresh-export',
        'internal-error',
        'no-open-run',
        'no-pending-intake-xml',
        'tree-registry-unusable',
        'tree-unconverged',
        'utf-8',
        'verified-snapshot',
    ],
}

NAMED_WITHOUT_OWN = {
    # 2026-11-05, U211: the scan's refusal for a process it could not read.
    'core/processes.py': ['rekordbox-absence-unconfirmed'],
    'core/backup_facts.py': ['grant-path-access', 'repair-backup-facts', 'upgrade-cratekit'],
    'core/binaries.py': [
        'fix-binary-override',
        'install-binary',
        'install-binary-source-unknown',
        'unsupported-platform',
    ],
    'core/config.py': ['upgrade-cratekit'],
    'core/jobs.py': ['cancelled'],
    # 2026-11-02, U193: the call ceiling's stop joined.
    # 2026-11-21, U293: the night pass's line joined.
    'core/provider_gate.py': ['provider-budget', 'provider-call-ceiling', 'provider-cooldown', 'provider-gate-held', 'provider-night-budget'],  # 2026-11-12, U278
    # 2026-11-21, U293: the staging lock joined.
    'core/staging_lock.py': ['staging-held'],
    'core/session.py': ['awaiting-import'],
}

NAMED_WITH_OWN = {
    # 2026-11-05, U211: the scan's refusal for a process it could not read.
    'core/processes.py': ['rekordbox-absence-unconfirmed'],
    'core/backup_facts.py': [
        'grant-path-access',
        'never-recorded',
        'recorded-in-the-future',
        'repair-backup-facts',
        'upgrade-cratekit',
    ],
    'core/binaries.py': [
        'fix-binary-override',
        'from-source',
        'install-binary',
        'install-binary-source-unknown',
        'unsupported-platform',
    ],
    # 2026-11-22, U299: the state inventory's literals moved to core/state_files.py,
    # and the pin's refusal to core/config_schema.py.
    'core/config.py': [
        'fix-config-values',
        'repair-config-file',
        'retry-when-unlocked',
        'run-setup',
        'upgrade-cratekit',
    ],
    'core/convergence.py': ['rows-moved-at-a-standstill', 'sequence-went-backward'],
    'core/exit_codes.py': [
        'acknowledge-backup',
        'answer-decision',
        'authenticate-provider',
        'change-policy-or-input',
        'complete-pending-action',
        'disable-cloud-sync',
        'fix-command-line',
        'install-module-extra',
        'mount-library-volume',
        'prepare-library-in-rekordbox',
        'quit-rekordbox',
        'rebuild-tree',
        'replan-then-decide',
        'report-defect',
        'restore-from-snapshot',
        'resume-job',
        'retry-later',
        'revalidate-pins',
        'run-doctor',
        'wait-for-holder',
    ],
    'core/jobs.py': ['cancelled'],
    'core/preflight.py': ['if-root-can-be-created', 'if-root-exists'],
    # 2026-11-02, U193: the call ceiling's stop joined.
    # 2026-11-21, U293: the night pass's line joined.
    'core/provider_gate.py': ['provider-budget', 'provider-call-ceiling', 'provider-cooldown', 'provider-gate-held', 'provider-night-budget'],  # 2026-11-12, U278
    'core/reconcile.py': ['in-flight-restore', 'unconverged-tree'],
    'core/restore.py': [
        'bare-metal-recovery',
        'clear-companion',
        'library-session',
        'mark-trees-unconverged',
        'record-reconciliation',
        'release-restore-latch',
        'remove-absent',
        'replace-directory',
        'replace-file',
        'resolve-session',
    ],
    # 2026-11-22, U301: core/review.py's entry left with the surfaces table.
    'core/routing.py': ['not-judged'],
    'core/secrets.py': ['install-keychain-backend', 'repair-credential-store', 'set-credential'],
    'core/state_files.py': [  # 2026-11-22, U299
        'downloaded-file',
        'never-restored',
        'remote-playlist-prefix',
        'survives-rollback',
        'trashed-file',
        'written-file-tag',
    ],
    # 2026-11-21, U293: the staging lock joined.
    'core/staging_lock.py': ['staging-held'],
    'core/session.py': ['awaiting-import', 'committed-unverified'],
}

NAMED_WITH_INTEGER = frozenset({
    # 2026-11-22, U299: core/config.py holds no exit code range integer since the split.
    'core/convergence.py',
    'core/exit_codes.py',
    'core/preflight.py',
    'core/reconcile.py',
})

LITERAL_HOLDERS = {
    'core/active_taxonomy.py': ['config-unusable', 'library-volume-unmounted'],
    'core/backup_facts.py': ['grant-path-access', 'repair-backup-facts', 'upgrade-cratekit'],
    'core/binaries.py': [
        'fix-binary-override',
        'install-binary',
        'install-binary-source-unknown',
        'unsupported-platform',
    ],
    'core/binary_refusal.py': ['yt-dlp-missing'],
    'core/config.py': ['upgrade-cratekit'],
    'core/convergence.py': ['library-fingerprint-unreadable', 'tree-convergence-unusable', 'tree-unconverged'],
    'core/discovery.py': ['internal-error'],
    'core/exit_codes.py': [
        'fix-binary-override',
        'grant-path-access',
        'install-binary',
        'install-binary-source-unknown',
        'repair-backup-facts',
        'unsupported-platform',
        'upgrade-cratekit',
    ],
    # 2026-11-22, U301: the drive loop moved to core/jobs_drive.py.
    'core/jobs.py': [
        'cancelled',
        'internal-error',
        'job-driver-held',
        'job-not-retryable',
        'job-schema-mismatch',
        'job-unknown',
        'no-evidence',
    ],
    'core/jobs_drive.py': ['internal-error', 'mixed-permanent-failures', 'unavailable-transient'],
    # 2026-11-05, U211: the scan's refusal for a process it could not read.
    'core/processes.py': ['rekordbox-absence-unconfirmed'],
    # 2026-11-02, U193: the call ceiling's stop joined.
    # 2026-11-21, U293: the night pass's line joined.
    'core/provider_gate.py': ['provider-budget', 'provider-call-ceiling', 'provider-cooldown', 'provider-gate-held', 'provider-night-budget'],  # 2026-11-12, U278
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/rb_copies.py': ['canary-read-failed'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/rb_nodes.py': ['mytag-category-template-missing', 'whitelist-violation'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/rb_removal.py': ['soft-delete-marker-unreadable', 'whitelist-violation'],
    # 2026-11-12, U267: the shared read's refusal of a use it was not made for.
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/rb_writer.py': [
        'app-version-pin-drift',
        'app-version-pin-unrecorded',
        'canary-read-failed',
        'cloud-sync-active',
        'cloud-sync-unreadable',
        'database-open-failed',
        'db-schema-pin-drift',
        'internal-error',
        'library-database-missing',
        'library-database-not-rekordbox',
        'library-directory-missing',
        'mytag-category-template-missing',
        'pyrekordbox-pin-drift',
        'rekordbox-running',
        'soft-delete-marker-unreadable',
        'whitelist-violation',
        'write-lock-held',
    ],
    'core/reconcile.py': ['restore-reconciliation-outstanding', 'restore-record-unusable'],
    # 2026-10-31, U162: the rehearsal area helper joined.
    'core/rehearsal.py': ['internal-error', 'output-exists'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/restore.py': [
        'internal-error',
        'rekordbox-running',
        'restore-discards-committed-work',
        'restore-step-failed',
        'snapshot-integrity-failed',
    ],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/restore_perform.py': [
        'internal-error',
        'restore-staging-occupied',
        'restore-step-failed',
    ],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/restore_recovery.py': ['recovery-target-refused'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/restore_retention.py': ['internal-error'],
    # 2026-11-23, R-1924: the files' half of a restore, refusing a record it cannot read.
    'core/restore_tags.py': ['restore-record-unusable'],
    'core/review.py': [
        'awaiting-human-action',
        'review-already-resolved',
        'review-file-unusable',
        'review-item-unknown',
        'review-option-unknown',
        'review-queue-undeclared',
        'review-schema-mismatch',
        'review-selection-invalid',
    ],
    # 2026-11-22, U301: the exchange and the grouping moved to modules of their own.
    'core/review_exchange.py': ['review-file-unusable'],
    'core/review_groups.py': ['review-selection-invalid'],
    'core/secrets.py': ['credential-index-unreadable'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/session.py': ['awaiting-import', 'internal-error', 'session-committed-unverified'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/session_ack.py': [
        'backup-acknowledgment-backup-too-old',
        'backup-acknowledgment-missing',
        'backup-acknowledgment-no-terminal',
        'backup-facts-unreadable',
        'internal-error',
    ],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/session_analysis.py': ['anlz-modified'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/session_holders.py': ['internal-error', 'session-lock-held'],
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/session_volumes.py': [
        'library-volume-mismatch',
        'library-volume-unmounted',
        'mapped-volume-mismatch',
        'mapped-volume-unmounted',
    ],
    # 2026-11-13, R-1677: the check's throwaway copy with no room joined.
    'core/snapshot.py': [
        'internal-error',
        'library-database-missing',
        'snapshot-check-temp-full',
        'snapshot-integrity-failed',
        'snapshot-store-full',
    ],
    # Re-pinned on the merge of main at e686759 (U125) into fable/300, 2026-10-10:
    # a new module, the taxonomy upgrade planner (U132). Measured on the merged tree.
    # 2026-11-21, U293: the staging lock joined.
    'core/staging_lock.py': ['staging-held'],
    'core/taxonomy_upgrade.py': ['config-unusable', 'internal-error'],
    'core/tombstone.py': ['review-selection-invalid'],
    'core/tree_registry.py': [
        'cutover-already-recorded',
        'cutover-export-missing',
        'cutover-native-write-taken',
        'cutover-open-run',
        'cutover-snapshot-missing',
        'cutover-xml-pending',
        'internal-error',
        'tree-registry-unusable',
        'tree-unconverged',
    ],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    # 2026-11-22, U299: core/config.py holds no exit code range integer since the split.
    'core/convergence.py',
    'core/exit_codes.py',
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/rb_nodes.py',
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/rb_removal.py',
    'core/reconcile.py',
    'core/rehearsal.py',  # 2026-10-31, U162: the rehearsal area helper joined.
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/restore_recovery.py',
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/restore_retention.py',
    'core/review.py',
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/session_ack.py',
    # 2026-11-22, U300: the split of rb_writer, session and restore moved it.
    'core/session_holders.py',
    'core/snapshot.py',
})
