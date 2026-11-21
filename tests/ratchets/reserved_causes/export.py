"""Reserved cause pins for ``export``, one entry per module (U125, U296).

Read by ``tests/_pinned_reserved_populations.py``, which says what each table
holds. When a pin fails, measure again on the merged tree, update only the
modules that moved, and put a dated comment on those entries.
"""

KEBAB_LITERALS = {
    # Re-pinned on the merge of main at 5b5dba2 into fable/299, 2026-10-10:
    # ONE kebab literal joined in export/cli.py and nothing left,
    # export-playlist-unfiled, the WARNING code for a new playlist U131 could
    # not file in Exports at creation. Measured on the merged tree; do not
    # bring back a package-wide total tuple. Re-pinned by U270, 2026-11-13:
    # internal-error joined, the one track export answering nothing for its
    # track, a defect the batched writer's single item form refuses.
    'export/cli.py': [
        'export-playlist-unfiled',
        'export-playlist-unknown',
        'export-tracks-unmatched',
        'internal-error',
        'outbound-item-absent',
        'outbound-playlist-adopted',
        'outbound-playlist-adoption-ambiguous',
        'outbound-playlist-record-mismatch',
    ],
    'export/prune_cli.py': ['export-playlist-unknown'],
    # Re-pinned on the merge of main at e686759 into grok/297, 2026-10-10:
    # SEVEN kebab literals joined in export/set_cli.py and nothing left,
    # credential-missing plus the six backfill and export-set codes U129 adds.
    'export/set_cli.py': [
        'credential-missing',
        'export-archive',
        'export-archive-backfill',
        'export-archive-backfill-refused',
        'export-archive-changed-since-plan',
        'export-archive-nothing-built',
        'export-set',
        'export-set-backfill',
        'export-set-backfill-no-job',
        'export-set-backfill-no-tracks',
        # 2026-10-13, U140: the set rename's refusal joined.
        'export-set-rename-unresolved',
        'export-set-tracks-refused',
        'intake-list-unusable',
        'internal-error',
        'library-isrc',
        'sync-mark-record-unusable',
        'taken-off',
        'unavailable-transient',
    ],
}

NAMED_WITHOUT_OWN = {
    # 2026-10-13, U140: the set rename's refusal, held in a named constant.
    'export/set_cli.py': ['export-set-rename-unresolved'],
}

NAMED_WITH_OWN = {
    # 2026-10-13, U140: the set rename's refusal, held in a named constant.
    'export/set_cli.py': ['export-set-rename-unresolved'],
}

LITERAL_HOLDERS = {
    # U270, 2026-11-13: internal-error joined, the one track export answering nothing.
    'export/cli.py': ['export-playlist-unknown', 'internal-error', 'outbound-item-absent'],
    'export/prune_cli.py': ['export-playlist-unknown'],
    # Re-pinned on the merge of main at e686759 into grok/297, 2026-10-10:
    # ONE cause literal joined in export/set_cli.py and nothing left,
    # credential-missing, the soft skip path U129's set backfill names.
    # 2026-10-13, U140: the set rename's refusal joined.
    'export/set_cli.py': [
        'credential-missing',
        'export-set-rename-unresolved',
        'intake-list-unusable',
        'internal-error',
        'sync-mark-record-unusable',
        'unavailable-transient',
    ],
}
