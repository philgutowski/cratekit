"""Reserved cause pins for ``modules.tools``, one entry per module (U125, U296).

Read and explained by ``tests/_pinned_reserved_populations.py``."""

KEBAB_LITERALS = {
    'modules/tools/__init__.py': ['restore-database'],
    'modules/tools/backup.py': [
        'analysis-share',
        'analysis-share-absent',
        'archive-listing-failed',
        'archive-purge-failed',
        'backup-record-not-kept',  # 2026-11-21, U317
        'backup-restore',
        'database-absent',
        'destination-not-configured',
        'library-root-absent',
        'library-root-foreign',  # 2026-11-21, #893
        'library-root-unproven',  # 2026-11-21, #893
        'list-share',
        'list-snapshot-contents',
        'list-snapshot-identity',
        'list-snapshots',
        'no-snapshot-available',
        'prune-archive',
        'prune-archive-folder',
        'quick-archive',  # 2026-11-21, U317
        'quick-resend',  # 2026-11-21, U317
        'quick-send',  # 2026-11-21, U317
        'rclone-missing',
        'rekordbox-absence-unconfirmed',  # 2026-11-05, U211.
        'rekordbox-running',
        'remote-not-configured',
        'restore-database',
        'restore-mirror',
        'restore-not-confirmed',
        'restore-share',
        'restore-target-absent',
        'restore-transfer-failed',
        'snapshot-database',
        'snapshot-identity',
        'snapshot-identity-not-written',
        'snapshot-identity-unrecorded',
        'snapshot-library-mismatch',
        'snapshot-listing-failed',
        'snapshot-name-invalid',
        'snapshot-settings',
        'snapshot-share',
    ],
    'modules/tools/backup_record.py': ['utf-8'],  # 2026-11-21, U317
    'modules/tools/mastering.py': [
        '24-bit',
        'archive-holds-a-different-recording',
        'archive-verify-failed',
        'drift-correction',
        'encoder-failed',
        'encoder-missing',
        'normalize-and-encode',
        'output-exists',
        'source-missing',
        'source-unsupported',
        'utf-8',
    ],
    'modules/tools/setbuilder.py': ['utf-8'],
}

NAMED_WITHOUT_OWN = {
    # 2026-11-22, U311: the rest moved with the restore side and the database
    # plan to backup_snapshot.py, whose Refusal names the reader resolves in
    # the declaring module only.
    'modules/tools/backup.py': [
        'destination-not-configured',
        'library-root-absent',
        'library-root-foreign',  # 2026-11-21, #893
        'library-root-unproven',  # 2026-11-21, #893
        'rclone-missing',
        'remote-not-configured',
        'restore-transfer-failed',
    ],
    'modules/tools/mastering.py': [
        'archive-holds-a-different-recording',
        'archive-verify-failed',
        'encoder-failed',
        'encoder-missing',
        'output-exists',
        'source-missing',
        'source-unsupported',
    ],
}

NAMED_WITH_OWN = {
    # 2026-11-22, U311: the rest moved with the restore side and the database
    # plan to backup_snapshot.py, whose Refusal names the reader resolves in
    # the declaring module only.
    'modules/tools/backup.py': [
        'destination-not-configured',
        'library-root-absent',
        'library-root-foreign',  # 2026-11-21, #893
        'library-root-unproven',  # 2026-11-21, #893
        'rclone-missing',
        'remote-not-configured',
        'restore-transfer-failed',
    ],
    'modules/tools/mastering.py': [
        'archive-holds-a-different-recording',
        'archive-verify-failed',
        'encoder-failed',
        'encoder-missing',
        'output-exists',
        'source-missing',
        'source-unsupported',
    ],
}

NAMED_WITH_INTEGER = frozenset({
    'modules/tools/mastering.py',
})

LITERAL_HOLDERS = {
    'modules/tools/backup.py': [
        'database-absent',
        'destination-not-configured',
        'library-root-absent',
        'library-root-foreign',  # 2026-11-21, #893
        'library-root-unproven',  # 2026-11-21, #893
        'no-snapshot-available',
        'rclone-missing',
        'rekordbox-absence-unconfirmed',  # 2026-11-05, U211.
        'rekordbox-running',
        'remote-not-configured',
        'restore-not-confirmed',
        'restore-target-absent',
        'restore-transfer-failed',
        'snapshot-identity-unrecorded',
        'snapshot-library-mismatch',
        'snapshot-listing-failed',
        'snapshot-name-invalid',
    ],
    'modules/tools/mastering.py': [
        'archive-holds-a-different-recording',
        'archive-verify-failed',
        'encoder-failed',
        'encoder-missing',
        'output-exists',
        'source-missing',
        'source-unsupported',
    ],
}

LITERAL_HOLDERS_WITH_INTEGER = frozenset({
    'modules/tools/mastering.py',
})
