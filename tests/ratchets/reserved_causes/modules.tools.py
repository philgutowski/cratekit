"""Reserved cause pins for ``modules.tools``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'modules/tools/__init__.py': ['restore-database'],
    'modules/tools/backup.py': [
        'analysis-share',
        'analysis-share-absent',
        'archive-listing-failed',
        'archive-purge-failed',
        'backup-restore',
        'database-absent',
        'destination-not-configured',
        'library-root-absent',
        'list-share',
        'list-snapshot-contents',
        'list-snapshot-identity',
        'list-snapshots',
        'no-snapshot-available',
        'prune-archive',
        'prune-archive-folder',
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
    'modules/tools/backup.py': [
        'database-absent',
        'destination-not-configured',
        'library-root-absent',
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

NAMED_WITH_OWN = {
    'modules/tools/backup.py': [
        'database-absent',
        'destination-not-configured',
        'library-root-absent',
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

NAMED_WITH_INTEGER = frozenset({
    'modules/tools/mastering.py',
})

LITERAL_HOLDERS = {
    'modules/tools/backup.py': [
        'database-absent',
        'destination-not-configured',
        'library-root-absent',
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
