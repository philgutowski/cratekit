"""Reserved cause pins for ``vocals``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    'vocals/cli.py': [
        'analysis-write-failed',
        'config-unusable',
        'folder-absent',
        'internal-error',
        'job-unknown',
        'module-extras-missing',
        'no-audio',
        'none-unscored',  # 2026-11-01, U181
        'source-missing',
    ],
}

LITERAL_HOLDERS = {
    'vocals/cli.py': [
        'analysis-write-failed',
        'config-unusable',
        'internal-error',
        'job-unknown',
        'module-extras-missing',
        'source-missing',
    ],
}
